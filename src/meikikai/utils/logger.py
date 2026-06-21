# meikikai/utils/logger.py
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from meikikai.config.config import APP_NAME

TRACE_LEVEL_NUM = 5
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")


def trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        self._log(TRACE_LEVEL_NUM, message, args, **kws)


logging.Logger.trace = trace

def setup_logging():
    log_formatter = logging.Formatter(
        f"%(asctime)s - [%(levelname)-5s] - [{APP_NAME}] - %(message)s",
        datefmt='%H:%M:%S'
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)

    log_dir = Path.home() / "Library" / "Logs" / APP_NAME
    log_dir.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        log_dir / "meikikai.log",
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(log_formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # logging.INFO or TRACE_LEVEL_NUM

    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)