import sys

from nmk_base.common import run_with_logs

from nmk.model.builder import NmkTaskBuilder
from nmk.model.keys import NmkRootConfig


class PackageBuilder(NmkTaskBuilder):
    def build(self, setup: str, artifacts: str):
        # Delegate to setup
        run_with_logs(
            [sys.executable, setup, "sdist", "-d", artifacts, "bdist_wheel", "-d", artifacts],
            self.logger,
            cwd=self.model.config[NmkRootConfig.PROJECT_DIR].value,
        )
