"""
Python version handling
"""

import platform
from typing import cast

from nmk.model.builder import NmkTaskBuilder
from nmk.model.resolver import NmkListConfigResolver, NmkStrConfigResolver
from setuptools_scm import get_version


class PythonVersionResolver(NmkStrConfigResolver):
    """
    Python version resolver
    """

    def get_value(self, name: str, root: str, version_scheme: str, local_scheme: str, fallback_version: str) -> str:  # type: ignore
        """
        Delegates to setuptools_scm to get the version from git
        """

        return get_version(root=root, version_scheme=version_scheme, local_scheme=local_scheme, fallback_version=fallback_version)


class PythonVersionRefresh(NmkTaskBuilder):
    """
    Python version builder
    """

    def build(self, version: str):  # type: ignore
        """
        Simple python version dump
        """
        self.logger.info(self.task.emoji, self.task.description)  # type: ignore
        with self.main_output.open("w") as f:
            f.write(version)


class PythonSupportedVersionsResolver(NmkListConfigResolver):
    """
    Supported python versions range resolver
    """

    def get_value(self, name: str) -> list[str]:
        """
        Returns supported python versions range

        :return: list of all python versions between min and max supported versions
        """

        def _split_version(v: str) -> list[int]:
            return list(map(int, v.split(".")))

        # Get min/max values, and verify consistency
        min_ver, max_ver = cast(tuple[str, str], (self.model.config["pythonMinVersion"].value, self.model.config["pythonMaxVersion"].value))
        min_split, max_split = _split_version(min_ver), _split_version(max_ver)
        prefix = "Inconsistency in python min/max supported versions: "
        assert len(min_split) == len(max_split), prefix + "not the same segments count"
        assert len(min_split) == 2, prefix + "can only deal with X.Y versions (2 segments expected)"
        assert min_split[0] == max_split[0], prefix + "can't deal with different major versions"
        assert max_split[1] > min_split[1], prefix + "max isn't greater than min"

        # Also verifies current runtime is in range
        p_ver = platform.python_version()
        cur_split = _split_version(p_ver)
        assert cur_split[0] == max_split[0], prefix + f"current python major version ({p_ver}) doesn't match with supported versions range"
        assert min_split[1] <= cur_split[1] <= max_split[1], prefix + f"current python version ({p_ver}) is out of supported versions range"

        # Iterate and return versions range
        return [f"{min_split[0]}.{sub}" for sub in range(min_split[1], max_split[1] + 1)]
