from flask import Blueprint, send_from_directory, current_app, jsonify
from pathlib import Path

import json

data_bp = Blueprint('data', __name__)

# =================
# ROBOTS
# =================
@data_bp.route('/robots.txt')
def robots():
    return send_from_directory(
        current_app.static_folder,
        'robots.txt',
        mimetype='text/plain'
    )