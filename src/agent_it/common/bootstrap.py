from configparser import ConfigParser
from pathlib import Path
import json

DATA_DIR = Path(r"C:\ProgramData\Agent_IT")

CONFIG_FILE = DATA_DIR / "Agent_IT.ini"
STATE_FILE = DATA_DIR / "agent_state.json"
LOG_DIR = DATA_DIR / "logs"


def create_default_config():

    config = ConfigParser()

    config["AGENT"] = {
        "name": "Agent_IT",
        "version": "0.1.0",
        "poll_interval": "30"
    }

    config["SERVER"] = {
        "host": "192.168.1.1",
        "port": "8000",
        "endpoint": "/events"
    }

    config["LOGGING"] = {
        "level": "INFO"
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        config.write(f)


def create_default_state():

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "last_record_id": 0
            },
            f,
            indent=4
        )


def initialize_environment():

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not CONFIG_FILE.exists():
        create_default_config()

    if not STATE_FILE.exists():
        create_default_state()