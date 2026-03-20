def register_routes(app):
    from .app_routes import main_bp
    from .file_routes import file_bp
    from .data_routes import data_bp
    from .debug_routes import debug_bp

    # Apply Blueprint
    app.register_blueprint(main_bp)         # App Routes
    app.register_blueprint(file_bp)         # File Routes
    app.register_blueprint(data_bp)         # Data Routes
    app.register_blueprint(debug_bp)        # Debug Routes