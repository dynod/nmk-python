"""
Python support for nmk
"""

from configparser import ConfigParser
from importlib.metadata import version
from pathlib import Path

from nmk_base.version import VersionResolver

__title__ = "nmk-python"
try:
    __version__ = version(__title__)
except Exception:  # pragma: no cover
    # For debug
    try:
        with (Path(__file__).parent.parent.parent / "setup.cfg").open("r") as f:
            c = ConfigParser()
            c.read_file(f.readlines())
            __version__ = c.get("metadata", "version")
    except Exception:
        __version__ = "unknown"


class NmkPythonVersionResolver(VersionResolver):
    """Plugin version resolver"""

    def get_version(self) -> str:
        """Returns nmk-python plugin version"""
        return __version__
