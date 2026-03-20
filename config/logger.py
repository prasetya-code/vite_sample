from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

import os, logging, atexit, socket, time, threading


# =====================================================
# GEO LOOKUP HELPER (MaxMind GeoLite2)
# =====================================================
# Membutuhkan: pip install geoip2
# Download DB: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
# Set env    : GEOIP_DB_PATH=/path/to/GeoLite2-City.mmdb
#
# Jika DB tidak tersedia, semua field geo akan fallback ke "-"
# =====================================================
_geo_reader      = None
_geo_reader_lock = threading.Lock()


def _get_geo_reader():
    """
    Lazy-load GeoIP reader (singleton, thread-safe).
    Hanya diinisialisasi sekali saat pertama kali dibutuhkan.
    """
    global _geo_reader
    if _geo_reader is None:
        with _geo_reader_lock:
            if _geo_reader is None:
                db_path = os.environ.get("GEOIP_DB_PATH", "GeoLite2-City.mmdb")
                try:
                    import geoip2.database
                    _geo_reader = geoip2.database.Reader(db_path)
                except Exception:
                    _geo_reader = False  # sentinel: sudah dicoba tapi gagal
    return _geo_reader if _geo_reader else None


def _lookup_geo(ip: str) -> dict:
    """
    Lookup geo info dari IP address.
    Return dict fallback (semua "-") jika gagal atau reader tidak tersedia.
    """
    fallback = {
        "country": "-", "city": "-",
        "region":  "-", "timezone": "-",
        "lat":     "-", "lon":      "-",
    }
    if not ip or ip in ("-", "127.0.0.1", "::1"):
        return fallback

    reader = _get_geo_reader()
    if reader is None:
        return fallback

    try:
        geo = reader.city(ip)
        return {
            "country":  geo.country.iso_code or "-",
            "city":     geo.city.name or "-",
            "region":   geo.subdivisions[0].name if geo.subdivisions else "-",
            "timezone": geo.location.time_zone or "-",
            "lat":      str(geo.location.latitude  or "-"),
            "lon":      str(geo.location.longitude or "-"),
        }
    except Exception:
        return fallback


# =====================================================
# REQUEST STATE — thread-local storage
# =====================================================
# Menyimpan state per-request secara thread-local sehingga
# aman dipakai di lingkungan multi-threaded (Werkzeug, Gunicorn threads).
#
# Field:
#   request_start_time → di-set saat request masuk (oleh IPFilter)
#   status_code        → di-set setelah response selesai (oleh after_request
#                        yang diregistrasi di dalam setup_logger)
# =====================================================
_tl = threading.local()


# =====================================================
# FLUSHING HANDLER
# =====================================================
class FlushingTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    Handler dengan auto-flush setiap kali ada log masuk,
    mencegah log tertahan di buffer I/O.
    """
    def emit(self, record):
        super().emit(record)
        self.flush()


# =====================================================
# IP FILTER
# =====================================================
class IPFilter(logging.Filter):
    """
    Filter untuk menyisipkan client IP ke setiap LogRecord.
    IP diambil dari Flask request context jika tersedia,
    fallback ke '-' jika dipanggil di luar request context.

    Sekaligus mencatat waktu mulai request ke thread-local (_tl)
    agar EnrichedFilter bisa menghitung response time tanpa middleware.
    """
    def filter(self, record):
        try:
            from flask import request

            record.client_ip = request.remote_addr or "-"

            # Catat waktu awal request jika belum ada untuk thread ini
            if not hasattr(_tl, "request_start_time"):
                _tl.request_start_time = time.time()

        except Exception:
            record.client_ip = "-"

        return True


# =====================================================
# ENRICHED FILTER
# =====================================================
class EnrichedFilter(logging.Filter):
    """
    Filter utama yang menyisipkan semua field tambahan ke setiap LogRecord.
    Dijalankan setelah IPFilter karena membutuhkan record.client_ip.

    Field yang ditambahkan:

    Geo & network  → country, city, region, timezone, lat, lon
    Request        → method, url, user_agent, referer,
                     request_id (dari header X-Request-ID),
                     status_code (dari after_request internal),
                     response_time (dari thread-local timer)
    Infra & runtime→ hostname, environment, app_version, pid, tid

    Semua field fallback ke '-' jika tidak tersedia — aman dipanggil
    baik di dalam maupun di luar Flask request context.
    """

    # ── Infra: dihitung sekali saat proses start ──────────────────────────
    _HOSTNAME    = socket.gethostname()
    _ENVIRONMENT = os.environ.get("APP_ENV",     "development")
    _APP_VERSION = os.environ.get("APP_VERSION", "unknown")

    def filter(self, record):

        # ── Geo enrichment dari client_ip (sudah di-set oleh IPFilter) ────
        geo = _lookup_geo(getattr(record, "client_ip", "-"))
        record.country  = geo["country"]
        record.city     = geo["city"]
        record.region   = geo["region"]
        record.timezone = geo["timezone"]
        record.lat      = geo["lat"]
        record.lon      = geo["lon"]

        # ── Request context (Flask) ───────────────────────────────────────
        try:
            from flask import request

            record.method     = request.method
            record.url        = request.url
            record.user_agent = request.headers.get("User-Agent", "-")
            record.referer    = request.referrer or "-"

            # request_id diambil langsung dari header X-Request-ID
            record.request_id = request.headers.get("X-Request-ID", "-")

            # response_time dihitung dari thread-local timer (diset IPFilter)
            start = getattr(_tl, "request_start_time", None)
            record.response_time = (
                str(round((time.time() - start) * 1000, 2)) if start else "-"
            )

            # status_code diambil dari thread-local yang diset oleh
            # after_request yang diregistrasi di dalam setup_logger()
            record.status_code = getattr(_tl, "status_code", "-")

        except Exception:
            record.method        = "-"
            record.url           = "-"
            record.user_agent    = "-"
            record.referer       = "-"
            record.request_id    = "-"
            record.response_time = "-"
            record.status_code   = "-"

        # ── Infra & runtime ───────────────────────────────────────────────
        record.hostname    = self._HOSTNAME
        record.environment = self._ENVIRONMENT
        record.app_version = self._APP_VERSION
        record.pid         = os.getpid()
        record.tid         = threading.get_ident()

        return True


# =====================================================
# LOG FORMAT
# =====================================================
# Struktur (tiap blok [...] adalah satu konteks):
#
#   [timestamp]
#   [request_id]                           → dari header X-Request-ID
#   [ip | country | city | lat,lon]        → network & geo
#   [File name, function name, code line]  → lokasi kode
#   [Method, Route]                        → request detail
#   LEVEL: message
#   [status_code]                          → response summary
#
# Contoh output:
#   [2026-03-11 14:23:01,123] [req-abc] [203.x.x.x|ID|Jakarta]
#   [File name app_routes.py, function name index, code line 20]
#   [Methode GET, Route http://127.0.0.1:5000/]    INFO:   Index page [200]
# =====================================================
_LOG_FORMAT = (
    "[%(asctime)s] "
    "[%(request_id)s] "
    "[%(client_ip)s] "
    "[Countrey: %(country)s, City: %(city)s]"
    "[Lat: %(lat)s, Long: %(lon)s]"
    "[File: %(filename)s, Function: %(funcName)s, Line: %(lineno)d] "
    "[Method: %(method)s, Route: %(url)s] "
    "\t%(levelname)s:\t%(message)s "
)


# =====================================================
# INTERNAL LOGGER FACTORY
# =====================================================
def _create_file_logger(log_name, level=logging.INFO, flask_app=None):
    """
    Factory internal untuk membuat logger berbasis file.

    Deteksi process:
    - Parent Werkzeug : FLASK_RUN_FROM_CLI=true, WERKZEUG_RUN_MAIN tidak ada
                        → skip, kembalikan logger tanpa handler
    - Child Werkzeug  : WERKZEUG_RUN_MAIN=true
                        → pasang handler
    - Production      : keduanya tidak ada (gunicorn, waitress, systemd, dll)
                        → pasang handler

    Parameter flask_app (opsional):
        Jika diberikan, after_request akan diregistrasi langsung ke app
        untuk menangkap status_code tanpa perlu middleware eksternal.
    """

    log_dir = "logs"

    try:
        os.makedirs(log_dir, exist_ok=True)

    except Exception as e:
        print(f"Gagal membuat direktori '{log_dir}': {e}")

    today_str = datetime.now().strftime("%Y-%m-%d")
    log_file  = f"{log_dir}/{log_name}_{today_str}.log"

    logger = logging.getLogger(log_name)
    logger.setLevel(level)

    # Parent process Werkzeug — biarkan kosong, child yang akan init handler
    is_werkzeug_parent = (
        os.environ.get("WERKZEUG_RUN_MAIN") is None
        and os.environ.get("FLASK_RUN_FROM_CLI") == "true"
    )

    if is_werkzeug_parent:
        return logger

    if not logger.handlers:
        handler = FlushingTimedRotatingFileHandler(
            filename=log_file,
            when="midnight",
            interval=1,
            backupCount=30,
            encoding='utf-8',
            utc=False
        )

        formatter = logging.Formatter(_LOG_FORMAT)

        handler.setFormatter(formatter)
        handler.setLevel(level)
        handler.suffix = "%Y-%m-%d"

        # IPFilter harus sebelum EnrichedFilter karena EnrichedFilter
        # membaca record.client_ip yang di-set oleh IPFilter
        handler.addFilter(IPFilter())
        handler.addFilter(EnrichedFilter())

        logger.propagate = False
        logger.addHandler(handler)

        # ── Registrasi after_request ke Flask app (jika diberikan) ────────
        # Menangkap status_code dari response dan menyimpannya ke thread-local
        # sehingga log berikutnya dalam request yang sama bisa membacanya.
        # Reset semua state thread-local setelah response selesai.
        if flask_app is not None:
            @flask_app.after_request
            def _capture_response(response):
                _tl.status_code         = response.status_code
                _tl.request_start_time  = getattr(_tl, "request_start_time", None)
                return response

            @flask_app.teardown_request
            def _reset_thread_local(_exc):
                # Bersihkan state agar tidak bocor ke request berikutnya
                # pada thread yang sama (keep-alive / thread pool)
                _tl.status_code        = "-"
                _tl.request_start_time = None

        def write_exit_lines():
            handler.stream.write("\n")
            handler.flush()

        atexit.register(write_exit_lines)

    return logger


# =====================================================
# APPLICATION LOGGER
# =====================================================
def setup_logger(flask_app=None):
    """
    Logger utama aplikasi.
    Dipanggil sekali di register_middleware() — jangan panggil di module level.

    Parameter flask_app:
        Wajib diberikan agar after_request & teardown_request bisa diregistrasi
        langsung ke dalam logger tanpa menyentuh file lain.

    Contoh pemanggilan:
        from app import create_app
        app = create_app()
        setup_logger(flask_app=app)
    """
    return _create_file_logger(
        log_name="record",
        level=logging.INFO,
        flask_app=flask_app
    )


# =====================================================
# CSP LOGGER
# =====================================================
def setup_csp_logger(flask_app=None):
    """
    Logger khusus untuk Content-Security-Policy report.
    File terpisah namun masih dalam direktori log yang sama.

    Parameter flask_app:
        Sama seperti setup_logger — opsional tapi dianjurkan.
    """
    return _create_file_logger(
        log_name="csp",
        level=logging.WARNING,
        flask_app=flask_app
    )


# =====================================================
# GETTER — gunakan ini di semua route dan module
# =====================================================
def get_logger():
    """
    Ambil logger utama yang sudah diinisialisasi.
    Aman dipanggil di module level — hanya lookup by name, tidak buat handler baru.
    """
    return logging.getLogger("record")


def get_csp_logger():
    """
    Ambil logger CSP yang sudah diinisialisasi.
    Aman dipanggil di module level — hanya lookup by name, tidak buat handler baru.
    """
    return logging.getLogger("csp")