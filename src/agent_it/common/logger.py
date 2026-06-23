import logging

from agent_it.common.config import (
    LOG_DIR
)

LOG_FILE = LOG_DIR / "agent_it.log"

logger = logging.getLogger(
    "Agent_IT"
)

logger.setLevel(
    logging.INFO
)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)

file_handler = logging.FileHandler(
    LOG_FILE,
    encoding="utf-8"
)

file_handler.setFormatter(
    formatter
)

logger.addHandler(
    file_handler
)