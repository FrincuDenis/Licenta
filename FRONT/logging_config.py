import logging
import logging.handlers

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create file handler
    file_handler = logging.handlers.RotatingFileHandler(
        'application.log', maxBytes=5 * 1024 * 1024, backupCount=2)
    file_handler.setLevel(logging.DEBUG)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
