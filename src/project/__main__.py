import structlog

from project.logging import configure_logging
from project.settings import get_settings


def main():
    # Load settings
    settings = get_settings()

    # Logging configuration (must be done before any logging is done)
    configure_logging(level=settings.log.level, format=settings.log.format)

    logger = structlog.get_logger(__name__)
    logger.info("Hello, world!")


if __name__ == "__main__":
    main()