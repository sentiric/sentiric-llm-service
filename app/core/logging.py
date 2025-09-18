import logging
import sys
import structlog
from app.core.config import settings

# Bu fonksiyon artık Go/Rust'takiler gibi service_name alacak.
def setup_logging(service_name: str, log_level: str, env: str):
    log_level = log_level.upper()

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        # YENİ: Her loga servis adını ekleyen işlemci.
        structlog.processors.add_static_data({"service": service_name}),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if env == "development":
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True)
        ]
    else:
        processors = shared_processors + [structlog.processors.JSONRenderer()]
    
    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    handler = logging.StreamHandler(sys.stdout)
    
    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(log_level)

    for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.handlers = [] 
        uvicorn_logger.propagate = True

    logger = structlog.get_logger(service_name) # Ana logger'a da ismi verelim.
    logger.info("Logging configured", log_level=log_level, environment=env)
    return logger

# Bu genel logger artık kullanılmayacak, her dosya kendi logger'ını alacak.
# logger = structlog.get_logger()