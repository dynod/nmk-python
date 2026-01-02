"""
Python build backend definition module
"""

from abc import ABC, abstractmethod
from pathlib import Path

from nmk.model.model import NmkModel


class PythonBuildBackend(ABC):
    """
    Python build backend interface

    :param model: NmkModel instance
    """

    def __init__(self, model: NmkModel):
        self._model = model
        self._env_backend = model.env_backend

    @abstractmethod
    def install_editable(self):  # pragma: no cover
        """
        Install current project as editable package
        """
        pass

    @abstractmethod
    def install_wheel(self, wheel_path: Path):  # pragma: no cover
        """
        Install current project built wheel
        """
        pass

    @abstractmethod
    def build_wheel(self, build_dir: Path, built_wheel_name: str, wheel_version: str) -> Path:  # pragma: no cover
        """
        Build current project wheel

        :param build_dir: temporary build folder
        :param built_wheel_name: name of the built wheel file
        :return: path to built wheel
        """
        pass

    @abstractmethod
    def uninstall_wheel(self, wheel_name: str):  # pragma: no cover
        """
        Uninstall specified wheel

        :param wheel_name: name of the wheel to uninstall
        """
        pass
