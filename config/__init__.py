def register_config(app): 
    from config.logger import setup_logger, setup_csp_logger, get_logger
    import os

    # Set Log
    setup_logger(flask_app=app)
    setup_csp_logger(flask_app=app)

    # Get App Log
    logger = get_logger()

    # Hanya log "Restart" ketika proses utama berjalan setelah restart
    os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    boundary = "=" * 15

    logger.info(f"{boundary} LOGGER STARTING POINT {boundary} \n")
    logger.info("Flask is restarting...")
    logger.info("Log Start ... \n")

    

    # Set Static Ver (aman di kedua process)
    from config.static_ver import apply_static_versioning
    apply_static_versioning(app)