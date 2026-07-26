import subprocess
from typing import Any

import pytest
from buildenv.__main__ import buildenv
from pytest_multilog import TestHelper


class TestTemplate(TestHelper):
    def test_template(self, monkeypatch: pytest.MonkeyPatch):
        # Fake a "no CI" environment
        monkeypatch.delenv("CI", raising=False)

        # Fake subprocess to catch git execution
        old_sub_process_run = subprocess.run

        def filter_git_command(args: list[str], *pargs: list[Any], **kwargs: dict[str, Any]) -> subprocess.CompletedProcess[str]:
            if args[0] == "git":
                return subprocess.CompletedProcess(args, 0, str(self.test_folder), "")
            return old_sub_process_run(args, *pargs, **kwargs)  # type: ignore

        monkeypatch.setattr(subprocess, "run", filter_git_command)

        # Prepare a project with uvx backend
        assert (
            buildenv(
                [
                    "install",
                    "--template",
                    "nmk.python",
                    "-p",
                    str(self.test_folder),
                    "--add",
                    "ruff",
                ]
            )
            == 0
        )

        # Check pyproject file is generated
        assert (self.test_folder / "pyproject.toml").is_file()
