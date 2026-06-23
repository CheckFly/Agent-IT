# common/version.py

from importlib.metadata import version

try:
    VERSION = version("Agent-IT")
except Exception:
    VERSION = "dev 0.1.0"