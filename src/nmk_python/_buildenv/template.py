from pathlib import Path

from buildenv.extension import BuildEnvRenderer
from jinja2 import Environment, PackageLoader
from nmk_base._buildenv.template import NmkBaseProjectTemplate, NmkConfigType, NmkReference

_ENV = Environment(loader=PackageLoader("nmk_python"))
_SRC_PATH = Path("src")


class NmkPythonProjectTemplate(NmkBaseProjectTemplate):
    """
    Template for **nmk-python** plugin project
    """

    @property
    def weight(self) -> int:
        # Top level plugin weight
        return 300

    @property
    def references(self) -> list[NmkReference]:
        return super().references + [NmkReference("nmk-python!plugin.yml", ["nmk-base!plugin.yml"])]

    @property
    def description(self) -> str:
        return "python nmk project"

    @property
    def preferred_backend(self):
        return "uv"

    @property
    def generated_files(self) -> set[Path]:
        return super().generated_files | set(
            [
                Path("pyproject.toml"),
                _SRC_PATH / self.python_module_name / "__init__.py",
                _SRC_PATH / self.python_module_name / "sample.py",
                _SRC_PATH / "tests" / "__init__.py",
                _SRC_PATH / "tests" / "test_sample.py",
            ]
        )

    @property
    def post_generation_tasks(self) -> list[str]:
        return super().post_generation_tasks + ["py.project"]

    @property
    def ignored_tasks(self) -> list[str]:
        # Only ignore requirements.txt for uv backend
        return super().ignored_tasks + (["py.req"] if self.info.backend_name == "uv" else [])

    @property
    def python_module_name(self) -> str:
        # Deduce the python module name from the project name
        return self.project_name.replace("-", "_")

    @property
    def comments(self) -> dict[str, str]:
        return super().comments | {
            "config.venvPkgDeps": "\nDevelopment dependencies (tools)",
            "config.venvArchiveDeps": "\nDevelopment dependencies (tools, from local files)",
            "config.pythonPackageRequirements": "\nPython package dependencies",
            "config.pythonProjectFileItems": "\nExtra project settings",
        }

    def handle_dependencies(self, packages: list[str]) -> dict[str, NmkConfigType]:
        # Iterate on packages
        other_refs: list[str] = []
        dep_refs: list[str] = []

        # Pre-filter non-dev dependencies
        for package in packages:
            # Check for dependency groups (no group means it's a regular dependency, otherwise it's a dev dependency)
            if ":" not in package:
                dep_refs.append(package)
            else:
                other_refs.append(package)

        # Delegate to normal processing
        config_items: dict[str, NmkConfigType] = super().handle_dependencies(other_refs)

        # Build settings
        if dep_refs:  # pragma: no branch
            config_items["pythonPackageRequirements"] = dep_refs

        return config_items

    def generate_extra_files(self, renderer: BuildEnvRenderer):
        # Generate source code templates
        keywords = {"python_module": self.python_module_name}
        renderer.render(_ENV, "src/__init__.py.jinja", sub_path=_SRC_PATH / self.python_module_name, keywords=keywords)
        renderer.render(_ENV, "src/__init__.py.jinja", sub_path=_SRC_PATH / "tests", keywords=keywords)
        renderer.render(_ENV, "src/sample.py.jinja", sub_path=_SRC_PATH / self.python_module_name, keywords=keywords)
        renderer.render(_ENV, "src/test_sample.py.jinja", sub_path=_SRC_PATH / "tests", keywords=keywords)

    @property
    def config_items(self) -> dict[str, NmkConfigType]:
        items = dict(super().config_items)
        items.update(
            {
                "pythonProjectFileItems": {"project": {"description": "Insert here a oneline description of your project"}},
            }
        )
        return items
