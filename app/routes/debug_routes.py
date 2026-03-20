from flask import Blueprint, current_app, request
from config.logger import get_logger, get_csp_logger

import time, hashlib

debug_bp = Blueprint('debug', __name__)

logger =  get_logger()
csp_logger = get_csp_logger()

# =========================
# CONTAINER ROUTES
# =========================

# Container Health
@debug_bp.route("/health")
def health():
    logger.info('Checking Container Health \n')
    return "Container Health Check"


# =========================
# POLICY ROUTES
# =========================

# CSP Report
@debug_bp.route('/csp-report', methods=['POST'])
def csp_report():
    """
    JSON-only CSP report endpoint.
    """
    if request.content_type not in (
        "application/csp-report",
        "application/json"
    ):
        return '', 204

    report = request.get_json(silent=True)
    if not report:
        return '', 204

    csp = report.get("csp-report") or report

    blocked = csp.get("blocked-uri", "")
    violated = csp.get("violated-directive", "")

    # Filter noise
    if blocked.startswith(("chrome-extension://", "moz-extension://")):
        return '', 204

    # Simple dedup (60s)
    key = hashlib.sha256(f"{blocked}{violated}".encode()).hexdigest()
    now = int(time.time())

    cache = current_app.config.setdefault("_CSP_CACHE", {})
    if key in cache and now - cache[key] < 60:
        return '', 204

    cache[key] = now

    # ⬅️ GUNAKAN CSP LOGGER
    csp_logger.warning("CSP VIOLATION: %s", csp)

    return '', 204


