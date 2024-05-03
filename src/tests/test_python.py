# Tests for python plugin
import shutil
import subprocess
from configparser import ConfigParser
from pathlib import Path
from typing import List

from nmk.tests.tester import NmkBaseTester
from nmk_base.venvbuilder import VenvUpdateBuilder

import nmk_python


class TestPythonPlugin(NmkBaseTester):
    @property
    def templates_root(self) -> Path:
        return Path(__file__).parent / "templates"

    def expected_supp_versions(self) -> List[str]:
        return ["3.8", "3.9", "3.10", "3.11"]

    def check_version(self, monkeypatch, git_version: str, expected_python_version: str):
        # Fake git subprocess behavior
        monkeypatch.setattr(
            subprocess, "run", lambda all_args, check, capture_output, text, encoding, cwd, errors: subprocess.CompletedProcess(all_args, 0, git_version, "")
        )
        self.nmk(self.prepare_project("ref_python.yml"), extra_args=["--print", "pythonVersion"])
        self.check_logs(f'Config dump: {{ "pythonVersion": "{expected_python_version}" }}')  # NOQA: B028

    def test_python_version(self, monkeypatch):
        self.check_version(monkeypatch, "\n", "")
        self.check_version(monkeypatch, "1.2.3", "1.2.3")
        self.check_version(monkeypatch, "1.2.3-dirty", "1.2.3+dirty")
        self.check_version(monkeypatch, "1.2.3-12-gb95312a", "1.2.3.post12+gb95312a")
        self.check_version(monkeypatch, "1.2.3-12-gb95312a-dirty", "1.2.3.post12+gb95312a.dirty")

    def fake_python_src(self, content: str = "", package: str = "fake", name: str = "fake.py"):
        # Prepare fake source python files to enable python tasks
        src = self.test_folder / "src" / package
        src.mkdir(parents=True, exist_ok=True)
        fake = src / name
        with fake.open("w") as f:
            f.write(content)

    def test_python_version_stamp(self):
        # Check python version is not generated (while no python files)
        self.nmk(self.prepare_project("ref_python.yml"), extra_args=["py.version"])
        assert not (self.test_folder / "out" / ".pythonversion").is_file()

        # Prepare fake source python files to enable python tasks
        self.fake_python_src()

        # Check python version is generated
        self.nmk(self.prepare_project("ref_python.yml"), extra_args=["py.version"])
        self.check_logs("Refresh python version")
        assert (self.test_folder / "out" / ".pythonversion").is_file()

    def test_python_setup_missing_config(self):
        # Prepare fake source python files to enable python tasks
        self.fake_python_src()
        shutil.copyfile(self.template("missing_var.cfg"), self.test_folder / "missing_var.cfg")
        self.nmk(
            self.prepare_project("setup_missing_var.yml"),
            extra_args=["py.setup"],
            expected_error=f"An error occurred during task py.setup build: Unknown config items referenced from template {self.test_folder / 'missing_var.cfg'}: unknownConfig",
        )

    def test_python_setup_ok(self):
        # Prepare fake source python files to enable python tasks
        self.fake_python_src()
        shutil.copyfile(self.template("setup1.cfg"), self.test_folder / "setup1.cfg")
        shutil.copyfile(self.template("setup2.cfg"), self.test_folder / "setup2.cfg")
        self.nmk(
            self.prepare_project("setup_ok.yml"),
            extra_args=["py.setup"],
        )
        assert (self.test_folder / "setup.py").is_file()
        generated_setup = self.test_folder / "setup.cfg"
        assert generated_setup.is_file()

        # Verify merged content
        with generated_setup.open() as f:
            c = ConfigParser()
            c.read_file(f.readlines())
        assert c.get("dummy", "foo") == "bar"
        assert c.get("dummy", "bar") == "venv"
        assert c.get("dummy", "other") == "1,2,3"
        assert c.get("dummy", "ymlcontributedvalue") == "foo"
        assert c.get("anotherSection", "foo") == "bar"
        assert c.get("anotherSection", "arrayofvalues") == "\nabc\ndef"

        # Verify supported python versions
        assert c.get("metadata", "classifiers") == "\n" + "\n".join([f"Programming Language :: Python :: {v}" for v in self.expected_supp_versions()])

    def test_python_format(self):
        # Prepare fake source python files to enable python tasks
        self.fake_python_src("import bbb\nimport aaa")
        p = self.prepare_project("ref_python.yml")
        self.nmk(p, extra_args=["py.format"])
        assert (self.test_folder / "out" / ".format").is_file()

        # Check incremental build
        self.nmk(p, extra_args=["py.format"])
        self.check_logs("[py.format]] DEBUG 🐛 - Task skipped, nothing to do")

    def test_python_flake(self):
        # Prepare fake source with flake errors
        self.fake_python_src("foo=foo")
        self.nmk(
            self.prepare_project("ref_python.yml"),
            extra_args=["py.analyze"],
            # Mixed / & \ on Windows (because pythonSrcFolders strings list is built with / even on Windows)
            expected_error=f"{Path('src')/'fake'/'fake.py'}:1:7: F821 undefined name 'foo'",
        )
        assert not (self.test_folder / "out" / ".flake").is_file()

        # Prepare fake source without errors
        self.fake_python_src("")
        self.nmk(self.prepare_project("ref_python.yml"), extra_args=["py.analyze"])
        assert (self.test_folder / "out" / ".flake").is_file()

    def test_python_build(self):
        # Prepare test project for python build
        self.fake_python_src("")
        self.nmk(self.prepare_project("ref_python.yml"), extra_args=["py.build"])
        archives = list((self.test_folder / "out" / "artifacts").glob("fake-*"))
        assert len(archives) == 2

    def test_python_test(self):
        # Prepare test project for python build
        self.fake_python_src(
            """
class TestSomething:
    def test_something(self):
        pass
""",
            package="tests",
            name="test_foo.py",
        )
        p = self.prepare_project("ref_python.yml")
        self.nmk(p, extra_args=["py.tests"])
        assert self.test_folder / "out" / "tests" / "report.xml"

        # Trigger again to cover clean code
        self.nmk(p, extra_args=["py.tests"])

    def test_plugin_version(self):
        self.nmk(self.prepare_project("ref_python.yml"), extra_args=["version"])
        self.check_logs(f"-  👉 nmk-python: {nmk_python.__version__}")

    def test_install_ok(self, monkeypatch):
        monkeypatch.setattr(VenvUpdateBuilder, "build", lambda _s, pip_args: None)

        # Prepare test project for python install
        self.fake_python_src("")
        self.nmk(self.prepare_project("ref_python.yml"), extra_args=["py.install"])

    def test_install_skipped(self, monkeypatch):
        monkeypatch.setattr("nmk_python.build.is_windows", lambda: True)

        # Prepare test project for python install
        self.fake_python_src("")
        self.nmk(self.prepare_project("ref_python.yml"), extra_args=["py.install", "--config", "pythonPackage=nmk"])
        self.check_logs("Can't install nmk while running nmk!")

    def test_supported_versions(self):
        def quote(a: str) -> str:
            return f'"{a}"'  # NOQA: B028

        # Check default supported versions
        self.nmk(self.prepare_project("ref_python.yml"), extra_args=["--print", "pythonSupportedVersions"])
        self.check_logs(f'Config dump: {{ "pythonSupportedVersions": [ {", ".join(map(quote, self.expected_supp_versions()))} ] }}')

    def test_invalid_supported_versions_inconsistent(self):
        # Inconsistent segments count
        self.nmk(
            self.prepare_project("supported_versions_inconsistent.yml"),
            extra_args=["--print", "pythonSupportedVersions"],
            expected_rc=1,
            expected_error="Error occurred while resolving config pythonSupportedVersions: Inconsistency in python min/max supported versions: not the same segments count",
        )

    def test_invalid_supported_versions_segments(self):
        # 3 segments count
        self.nmk(
            self.prepare_project("supported_versions_3_segments.yml"),
            extra_args=["--print", "pythonSupportedVersions"],
            expected_rc=1,
            expected_error="Error occurred while resolving config pythonSupportedVersions: Inconsistency in python min/max supported versions: can only deal with X.Y versions (2 segments expected)",
        )

    def test_invalid_supported_versions_different_major(self):
        # Different major versions
        self.nmk(
            self.prepare_project("supported_versions_different.yml"),
            extra_args=["--print", "pythonSupportedVersions"],
            expected_rc=1,
            expected_error="Error occurred while resolving config pythonSupportedVersions: Inconsistency in python min/max supported versions: can't deal with different major versions",
        )

    def test_invalid_supported_versions_lower_max(self):
        # Lower max
        self.nmk(
            self.prepare_project("supported_versions_lower_max.yml"),
            extra_args=["--print", "pythonSupportedVersions"],
            expected_rc=1,
            expected_error="Error occurred while resolving config pythonSupportedVersions: Inconsistency in python min/max supported versions: max isn't greater than min",
        )

    def escape(self, to_escape: Path) -> str:
        # Escape backslashes (for Windows paths in json print)
        return str(to_escape).replace("\\", "\\\\")

    def test_files(self):
        # Basic setup
        prj_file = self.prepare_project("with_files_def.yml")
        self.fake_python_src()
        self.fake_python_src(package="codegen", name="foo.py")
        self.fake_python_src(package="tests", name="test.py")

        # Check source files breakdown in variables
        self.nmk(
            prj_file,
            extra_args=["--print", "pythonFoundSrcFiles", "--print", "pythonTestSrcFiles", "--print", "pythonGeneratedSrcFiles"],
        )
        self.check_logs(
            f'Config dump: {{ "pythonTestSrcFiles": [ "{self.escape(self.test_folder/"src"/"tests"/"test.py")}" ], '  # NOQA: B028
            + f'"pythonGeneratedSrcFiles": [ "{self.escape(self.test_folder)}/src/codegen/foo.py" ], '  # NOQA: B028
            + f'"pythonFoundSrcFiles": [ "{self.escape(self.test_folder/"src"/"fake"/"fake.py")}" ] }}'  # NOQA: B028
        )
