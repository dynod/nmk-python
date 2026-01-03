# Changelog

Here are listed all the meaningfull changes done on **`nmk-python`** since version 1.0

```{note}
Only interface and important behavior changes are listed here.

The fully detailed changelog is also available on [Github](https://github.com/dynod/nmk-python/releases)
```

## Release 1.8.0

- added {ref}`${pythonLocalDepsPatterns}<pythonLocalDepsPatterns>` config item to identify local dependencies that are in the same development workspace than the current project
- added {ref}`${pythonDepsMetadata}<pythonDepsMetadata>` config item pointing to generated dependencies metadata file
- updated **{ref}`py.uninstall<py.uninstall>`** task to additionally uninstall local dependencies
- added **{ref}`py.deps<py.deps>`** task to generated dependencies metadata

## Release 1.7.0

- removed **{ref}`py.version<py.version>`** and **{ref}`py.project<py.project>`** trigger condition (tasks are always executed, even if no python files were found in project)
- added {ref}`${pythonDevRequirements}<pythonDevRequirements>` and {ref}`${pythonArchiveRequirements}<pythonArchiveRequirements>` config items to ease **dev** dependency group generation
- renamed `${pythonEditableInstallArgs}` config item to {ref}`${pythonEditablePipInstallArgs}<pythonEditablePipInstallArgs>` one
- renamed `${pythonWheelInstallArgs}` config item to {ref}`${pythonWheelPipInstallArgs}<pythonWheelPipInstallArgs>` one
- added {ref}`${pythonEditableUvInstallArgs}<pythonEditableUvInstallArgs>` and {ref}`${pythonWheelUvInstallArgs}<pythonWheelUvInstallArgs>` config items to provide extra args for build with **uv** tool
- in generated **pyproject.toml**, add a **dependency-groups** section with a **dev** group holding all tools dependencies (as [required by uv tool](https://docs.astral.sh/uv/concepts/projects/dependencies/#development-dependencies))
- add override of [${venvUpdateInput}](https://nmk-base.readthedocs.io/en/stable/config.html#venvupdateinput) to condition venv refresh on **pyproject.toml** file
- refactored builders to introduce "build backend" logic and separate implementations:
  - the legacy one based on **pip** and python **build** module
  - a new one based on **uv** tool, ready for **buildenv** 2 compatibility

## Release 1.6.0

- added `--show-capture=no` pytest default option to {ref}`${pytestExtraArgs}<pytestExtraArgs>` config item
- updated supported versions range to 3.10-3.14 (see {ref}`${pythonMinVersion}<pythonMinVersion>` and {ref}`${pythonMaxVersion}<pythonMaxVersion>` config items)

## Release 1.5.0

- new {ref}`${pythonBuildExcludedModules}<pythonBuildExcludedModules>` config item to list modules to be excluded from the python wheel build

## Release 1.4.0

- generate [pyright](https://microsoft.github.io/pyright/#/) type checking tool configuration in **pyproject.toml**. The {ref}`${pythonTypeCheckingMode}<pythonTypeCheckingMode>` config item can be used to set the rule set to be used.

## Release 1.3.0

- handle python package optional dependencies through {ref}`${pythonPackageOptionalRequirements}<pythonPackageOptionalRequirements>` new config item

## Release 1.2.0

- new **{ref}`py.fix<py.fix>`** build task to auto-fix python code through [ruff](https://docs.astral.sh/ruff/linter/#fixes)
- new config items to specify extra args for ruff command lines:
  - {ref}`${pythonRuffCommonExtraArgs}<pythonRuffCommonExtraArgs>`
  - {ref}`${pythonRuffFormatExtraArgs}<pythonRuffFormatExtraArgs>`
  - {ref}`${pythonRuffFixExtraArgs}<pythonRuffFixExtraArgs>`
  - {ref}`${pythonRuffCheckExtraArgs}<pythonRuffCheckExtraArgs>`
- new {ref}`${pythonRuffFixStamp}<pythonRuffFixStamp>` config item (used for **{ref}`py.fix<py.fix>`**) incremental build
- new config items fto list rules to be auto-fixed:
  - {ref}`${pythonAutoFixRules}<pythonAutoFixRules>` (list version)
  - {ref}`${pythonAutoFixJoinedRules}<pythonAutoFixJoinedRules>` (string version)

## Release 1.1.0

- new `${pythonEditableInstallArgs}` config item
- new `${pythonWheelInstallArgs}` config item
- changed **{ref}`py.install<py.install>`** and **{ref}`py.editable<py.editable>`** tasks pip install args to point to these new items
