# Tests for python plugin
import platform
import subprocess
import sysconfig
from json import dumps
from pathlib import Path

from nmk.tests.tester import NmkBaseTester
from nmk_base.venvbuilder import VenvUpdateBuilder

import nmk_python


class TestPythonPlugin(NmkBaseTester):
    @property
    def templates_root(self) -> Path:
        return Path(__file__).parent / "templates"

    def expected_supp_versions(self) -> list[str]:
        return ["3.8", "3.9", "3.10", "3.11", "3.12"]

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

    def fake_python_src(self, content: str = "", package: str = "fake", name: str = "fake.py", with_init=False):
        # Prepare fake source python files to enable python tasks
        src = self.test_folder / "src" / package
        src.mkdir(parents=True, exist_ok=True)
        fake = src / name
        with fake.open("w") as f:
            f.write(content)
        if with_init:
            init = src / "__init__.py"
            init.touch()

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

    def test_python_format(self):
        # Prepare fake source python files to enable python tasks
        self.fake_python_src("import bbb\nimport aaa")
        p = self.prepare_project("ref_python.yml")
        self.nmk(p, extra_args=["py.format"])
        assert (self.test_folder / "out" / ".ruff-format").is_file()

        # Check incremental build
        self.nmk(p, extra_args=["py.format"])
        self.check_logs("[py.format]] DEBUG 🐛 - Task skipped, nothing to do")

    def test_python_analysis(self):
        # Prepare fake source with errors
        self.fake_python_src("foo=foo")
        self.nmk(
            self.prepare_project("ref_python.yml"),
            extra_args=["py.analyze"],
            # Mixed / & \ on Windows (because pythonSrcFolders strings list is built with / even on Windows)
            expected_error="An error occurred during task py.analyze build: command returned 1",
        )
        assert not (self.test_folder / "out" / ".ruff-check").is_file()

        # Prepare fake source without errors
        self.fake_python_src("")
        self.nmk(self.prepare_project("ref_python.yml"), extra_args=["py.analyze"])
        assert (self.test_folder / "out" / ".ruff-check").is_file()

    def test_python_build(self):
        # Prepare test project for python build
        self.fake_python_src("")
        project = self.prepare_project("ref_python.yml")
        self.nmk(project, extra_args=["py.build"])
        archives = list((self.test_folder / "out" / "artifacts").glob("fake-*"))
        assert len(archives) == 1
        assert (self.test_folder / "pyproject.toml").is_file()

        # Another build
        self.nmk(project, extra_args=["py.build"])
        self.check_logs("nothing to do")

        # Another build (forces)
        self.nmk(project, extra_args=["py.build", "-f"])
        archives = list((self.test_folder / "out" / "artifacts").glob("fake-*"))
        assert len(archives) == 1

    def test_python_build_platform_specific(self):
        # Prepare test project for python build
        self.fake_python_src("", with_init=True)
        project = self.prepare_project("ref_python.yml")
        some_fake_resources = self.test_folder / "foo.lib"
        some_fake_resources.touch()
        some_fake_folder = self.test_folder / "resources"
        some_fake_folder.mkdir()
        (some_fake_folder / "blablabla").touch()

        # Build for platform, with extra resource
        platform = sysconfig.get_platform().replace("-", "_")
        self.nmk(
            project,
            extra_args=[
                "py.build",
                "--config",
                f"pythonPackagePlatform={platform}",
                "--config",
                dumps({"pythonExtraResources": {some_fake_resources.name: "src/fake", some_fake_folder.name: "src/fake/extra"}}, indent=None),
            ],
        )
        archives = list((self.test_folder / "out" / "artifacts").glob(f"fake-*-{platform}.whl"))
        assert len(archives) == 1

        # Verify copied resources
        build = self.test_folder / "out" / "python" / "src" / "fake"
        assert (build / "foo.lib").is_file()
        assert (build / "extra" / "blablabla").is_file()

        # Check logs for extra resource bundling
        self.check_logs("adding 'fake/foo.lib'")

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

    def test_uninstall(self):
        # Simple pip call with sample package
        self.fake_python_src("")
        self.nmk(self.prepare_project("ref_python.yml"), extra_args=["py.uninstall"])
        self.check_logs("'-m', 'pip', 'uninstall', '--yes', 'fake'")

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

    def test_current_version_not_compatible(self, monkeypatch):
        # Fake python version
        monkeypatch.setattr(platform, "python_version", lambda: "2.7")
        self.nmk(
            self.prepare_project("project_ok.yml"),
            extra_args=["--print", "pythonSupportedVersions"],
            expected_rc=1,
            expected_error="Error occurred while resolving config pythonSupportedVersions: Inconsistency in python min/max supported versions: current python major version (2.7) doesn't match with supported versions range",
        )
        monkeypatch.setattr(platform, "python_version", lambda: "3.6")
        self.nmk(
            self.prepare_project("project_ok.yml"),
            extra_args=["--print", "pythonSupportedVersions"],
            expected_rc=1,
            expected_error="Error occurred while resolving config pythonSupportedVersions: Inconsistency in python min/max supported versions: current python version (3.6) is out of supported versions range",
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
            f'Config dump: {{ "pythonTestSrcFiles": [ "{self.escape(self.test_folder / "src" / "tests" / "test.py")}" ], '  # NOQA: B028
            + f'"pythonGeneratedSrcFiles": [ "{self.escape(self.test_folder)}/src/codegen/foo.py" ], '  # NOQA: B028
            + f'"pythonFoundSrcFiles": [ "{self.escape(self.test_folder / "src" / "fake" / "fake.py")}" ] }}'  # NOQA: B028
        )
