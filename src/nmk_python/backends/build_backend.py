"""
Python build backend definition module
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import cast

from nmk.envbackend import EnvBackend
from nmk.model.model import NmkModel


class PythonBuildBackend(ABC):
    """
    Python build backend interface

    :param model: NmkModel instance
    """

    def __init__(self, model: NmkModel):
        self._model = model
        self._env_backend = cast(EnvBackend, model.env_backend)  # type: ignore

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
    def uninstall_wheels(self):  # pragma: no cover
        """
        Uninstall wheels (i.e. restore venv in editable mode)
        """
        pass
