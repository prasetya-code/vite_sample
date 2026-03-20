from flask import Blueprint, render_template

from config.logger import get_logger

main_bp = Blueprint('main', __name__)

logger = get_logger()

# =========================
# APP ROUTES
# =========================

@main_bp.route("/")
def index():
    logger.info("Index page")
    return render_template("app/index.html")


# =========================
# HANDLER
# =========================

@main_bp.app_errorhandler(429)
def ratelimit_handler(e):
    return "Passed Rate Limit", 429

@main_bp.app_errorhandler(405)
def method_not_allowed_handler(e):
    return "Method Not Allowed", 405