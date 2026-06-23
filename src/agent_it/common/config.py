from configparser import ConfigParser
from pathlib import Path

from importlib.metadata import version

AGENT_NAME = "Agent_IT"
AGENT_VERSION = version("Agent-IT")

DATA_DIR = Path(r"C:\ProgramData\Agent_IT")

CONFIG_FILE = DATA_DIR / "Agent_IT.ini"
STATE_FILE = DATA_DIR / "agent_state.json"
LOG_DIR = DATA_DIR / "logs"

config = ConfigParser()
config.read(CONFIG_FILE)

AGENT_NAME = config.get(
    "AGENT",
    "name",
    fallback=AGENT_NAME
)

AGENT_VERSION = config.get(
    "AGENT",
    "version",
    fallback=AGENT_VERSION
)

POLL_INTERVAL = config.getint(
    "AGENT",
    "poll_interval",
    fallback=30
)

SERVER_HOST = config.get(
    "SERVER",
    "host",
    fallback="192.168.1.1"
)

SERVER_PORT = config.getint(
    "SERVER",
    "port",
    fallback=8000
)

SERVER_ENDPOINT = config.get(
    "SERVER",
    "endpoint",
    fallback="/events"
)

SERVER_URL = (
    f"http://{SERVER_HOST}:"
    f"{SERVER_PORT}"
    f"{SERVER_ENDPOINT}"
)

LOG_LEVEL = config.get(
    "LOGGING",
    "level",
    fallback="INFO"
)