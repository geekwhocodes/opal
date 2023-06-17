import logging
import sys
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel

LOGGER_FILE = Path("logd.log")  # where log is stored
DATE_FORMAT = "%d %b %Y | %H:%M:%S"
LOGGER_FORMAT = "%(asctime)s | %(message)s"

class LoggerConfig(BaseModel):
    handlers: list
    format: str
    date_format: str | None = None
    logger_file: Path | None = None
    level: int = logging.INFO

@lru_cache
def get_logger_config():
    """Installs RichHandler (Rich library) if not in production
    environment, or use the production log configuration.
    """
    if not "settings.env" == "prd":
        from rich.logging import RichHandler

        output_file_handler = logging.FileHandler(LOGGER_FILE)
        handler_format = logging.Formatter(
            LOGGER_FORMAT, datefmt=DATE_FORMAT)
        output_file_handler.setFormatter(handler_format)

        return LoggerConfig(
            handlers=[
                RichHandler(
                    rich_tracebacks=True,
                    tracebacks_show_locals=True,
                    show_time=False
                ),
                output_file_handler
            ],
            format=LOGGER_FORMAT,
            date_format=DATE_FORMAT,
            logger_file=LOGGER_FILE,
        )

    output_file_handler = logging.FileHandler(LOGGER_FILE)
    handler_format = logging.Formatter(
        LOGGER_FORMAT, datefmt=DATE_FORMAT)
    output_file_handler.setFormatter(handler_format)

    # Stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(handler_format)

    return LoggerConfig(
        handlers=[output_file_handler, stdout_handler],
        format="%(levelname)s: %(asctime)s \t%(message)s",
        date_format="%d-%b-%y %H:%M:%S",
        logger_file=LOGGER_FILE,
    )


def setup_logging():
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
        
    logger_config = get_logger_config()
    logging.basicConfig(
        level=logger_config.level,
        format=logger_config.format,
        datefmt=logger_config.date_format,
        handlers=logger_config.handlers,
    )