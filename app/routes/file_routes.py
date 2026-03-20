from flask import Blueprint, send_from_directory, abort, current_app

from app.utils.protected_manager import is_trusted_referer, is_allowed_file, is_safe_path
from app.utils.well_known_manager import ensure_well_known

from config.logger import get_logger
from pathlib import Path

logger = get_logger()
file_bp = Blueprint('file', __name__)

# ============================================================
# ✅ Helper function untuk serving file private
# ============================================================
def serve_private_file(file_type: str, filename: str, base_subdir: str):
    """
    Mengamankan dan melayani file dari folder private.
    - file_type: 'images', 'audio', 'files'
    - filename: nama file diminta
    - base_subdir: folder di dalam 'private' sesuai tipe
    """
    
    # Folder absolut
    base_dir = Path(current_app.root_path) / 'private' / base_subdir
    file_path = base_dir / filename

    # Validasi path aman
    if not is_safe_path(file_path, base_dir):
        logger.warning(f"Invalid path access: {file_path}")
        abort(403)

    # Validasi ekstensi
    if not is_allowed_file(filename, file_type):
        logger.warning(f"Extension not allowed: {filename}")
        abort(403)

    # Validasi referer
    if not is_trusted_referer(file_type):
        logger.warning(f"Referrer is not trusted for {filename}")
        abort(403)

    # Jika semua berhasil
    logger.info(f"Validation conditions have been met, {file_type} file: {file_path}")

    return send_from_directory(base_dir, filename)


# ============================================================
# Routes
# ============================================================

# Images
@file_bp.route('/images/<path:filename>')
def protected_image(filename):
    return serve_private_file('images', filename, 'images')


# Files
@file_bp.route('/files/<path:filename>')
def protected_files(filename):
    return serve_private_file('files', filename, 'files')


# Animation
@file_bp.route('/animate/<path:filename>')
def protected_animate(filename):
    return serve_private_file('animate', filename, 'animate')


# .well-known
@file_bp.route('/.well-known/<path:filename>')
def serve_well_known(filename):
    """
    Melayani file dari folder static/.well-known/
    dan membuat folder serta file default jika belum ada.
    """
    static_dir = Path(current_app.static_folder)
    well_known_dir = static_dir / ".well-known"

    # Pastikan folder dan file sudah ada
    ensure_well_known()

    # Sanitasi path agar aman
    file_path = (well_known_dir / filename).resolve()
    if not str(file_path).startswith(str(well_known_dir.resolve())):
        logger.warning(f"Unauthorized access attempt to .well-known: {filename} file: {file_path}")
        abort(403)

    # Jika file tidak ditemukan, kembalikan 204 (tidak error 404)
    if not file_path.exists():
        logger.info(f"File .well-known not found: {filename} file: {file_path}")
        return '', 204

    logger.info(f"Serving file .well-known: {filename}")

    return send_from_directory(well_known_dir, filename)