import sys

from nmk.model.builder import NmkTaskBuilder
from nmk.model.keys import NmkRootConfig
from nmk.model.resolver import NmkStrConfigResolver
from nmk.utils import run_with_logs


class PackageBuilder(NmkTaskBuilder):
    def build(self, setup: str, artifacts: str):
        # Delegate to setup
        run_with_logs(
            [sys.executable, setup, "sdist", "-d", artifacts, "bdist_wheel", "-d", artifacts],
            self.logger,
            cwd=self.model.config[NmkRootConfig.PROJECT_DIR].value,
        )


class PythonPackageForWheel(NmkStrConfigResolver):
    def get_value(self, name: str) -> str:
        return self.model.config["pythonPackage"].value.replace("-", "_")
