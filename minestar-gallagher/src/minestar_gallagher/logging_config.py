import structlog
import logging
import sys

def setup_logging():
    """Basic structured logging setup"""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
    )

    return structlog.get_logger()

# Call this early in main.py or service.py
logger = setup_logging()