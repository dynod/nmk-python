"""
Uv build backend module.
"""

from pathlib import Path

from .build_backend import PythonBuildBackend


class UvBuildBackend(PythonBuildBackend):
    """
    Uv build backend implementation

    :param model: NmkModel instance
    """

    def install_wheel(self, wheel_path: Path):
        # Prepare install args
        install_args = ["pip", "install", str(wheel_path)]

        # Delegate to subprocess
        self._env_backend.subprocess(install_args, cwd=self._env_backend.project_path)

    def build_wheel(self, build_dir: Path, built_wheel_name: str, wheel_version: str) -> Path:
        # Name for wheel sub-directory
        wheel_sub_dir = "wheel_dist"

        # Delegate to uv
        build_args = ["build", "--wheel", "--out-dir", wheel_sub_dir]
        self._env_backend.subprocess(build_args, cwd=build_dir)

        # Return built wheel path
        return build_dir / wheel_sub_dir / built_wheel_name

    def uninstall_wheels(self):
        # Same as setup, just don't print updates (will be done by uninstall builder)
        self._env_backend.upgrade(full=False)
