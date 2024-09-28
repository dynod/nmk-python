"""
Python version handling
"""

import re

from nmk.model.builder import NmkTaskBuilder
from nmk.model.resolver import NmkStrConfigResolver

# Git version pattern
_GIT_VERSION_PATTERN = re.compile("([^-]+)(?:-([0-9]+))?(?:-(.+))?")


class PythonVersionResolver(NmkStrConfigResolver):
    """
    Python version resolver
    """

    def get_value(self, name: str) -> str:
        """
        Turn the git version in the Python way
        """
        git_version = self.model.config["gitVersion"].value
        m = _GIT_VERSION_PATTERN.match(git_version)
        if m is not None:
            # Build python version from git version segments
            out = m.group(1)
            if m.group(2) is not None:
                # Add commits count
                out += f".post{m.group(2)}"
            if m.group(3) is not None:
                # Add hash/dirty
                out += f"+{m.group(3)}".replace("-", ".")
            return out

        # Probably a simpler version (without segments)
        # Assume it is already compliant...
        return git_version


class PythonVersionRefresh(NmkTaskBuilder):
    """
    Python version builder
    """

    def build(self, version: str):
        """
        Simple python version dump
        """
        self.logger.info(self.task.emoji, self.task.description)
        with self.main_output.open("w") as f:
            f.write(version)
