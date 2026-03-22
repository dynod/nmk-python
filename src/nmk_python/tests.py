"""
Python tests builder
"""

import shutil
import subprocess
import sys
from typing import cast

from nmk.model.builder import NmkTaskBuilder
from nmk.model.keys import NmkRootConfig


class PytestBuilder(NmkTaskBuilder):
    """
    Python tests builder
    """

    def build(self, pytest_args: dict[str, str | bool], ignore_failures: bool = False):  # type: ignore
        """
        Invoke pytest with specified options

        :param pytest_args: extra pytest command line args
        :param ignore_failures: whether to ignore test failures
        """

        # Clean outputs
        for p in self.outputs:
            if p.is_dir():
                shutil.rmtree(p)
            elif p.is_file():  # pragma: no cover
                p.unlink()

        # Compute extra args
        args: list[str] = []
        for opt_k, opt_v in pytest_args.items():
            if isinstance(opt_v, bool):
                if opt_v:
                    # Simple option
                    args.append(f"--{opt_k}")
            else:
                # Key + value
                args.append(f"--{opt_k}={opt_v}")

        # Invoke pytest
        all_args = [sys.executable, "-m", "pytest"] + args
        self.logger.debug(f"Running subprocess: {' '.join(all_args)}")
        subprocess.run(all_args, check=not ignore_failures, cwd=cast(str, self.model.config[NmkRootConfig.PROJECT_DIR].value))
