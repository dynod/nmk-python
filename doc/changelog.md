# Changelog

Here are listed all the meaningfull changes done on **`nmk-python`** since version 1.0

```{note}
Only interface and important behavior changes are listed here.

The fully detailed changelog is also available on [Github](https://github.com/dynod/nmk-python/releases)
```

## Release 1.6.0

* added `--show-capture=no` pytest default option to {ref}`${pytestExtraArgs}<pytestExtraArgs>` config item
* updated supported versions range to 3.10-3.14 (see {ref}`${pythonMinVersion}<pythonMinVersion>` and {ref}`${pythonMaxVersion}<pythonMaxVersion>` config items)

## Release 1.5.0

* new {ref}`${pythonBuildExcludedModules}<pythonBuildExcludedModules>` config item to list modules to be excluded from the python wheel build

## Release 1.4.0

* generate [pyright](https://microsoft.github.io/pyright/#/) type checking tool configuration in **pyproject.toml**. The {ref}`${pythonTypeCheckingMode}<pythonTypeCheckingMode>` config item can be used to set the rule set to be used.

## Release 1.3.0

* handle python package optional dependencies through {ref}`${pythonPackageOptionalRequirements}<pythonPackageOptionalRequirements>` new config item

## Release 1.2.0

* new **{ref}`py.fix<py.fix>`** build task to auto-fix python code through [ruff](https://docs.astral.sh/ruff/linter/#fixes)
* new config items to specify extra args for ruff command lines:
  * {ref}`${pythonRuffCommonExtraArgs}<pythonRuffCommonExtraArgs>`
  * {ref}`${pythonRuffFormatExtraArgs}<pythonRuffFormatExtraArgs>`
  * {ref}`${pythonRuffFixExtraArgs}<pythonRuffFixExtraArgs>`
  * {ref}`${pythonRuffCheckExtraArgs}<pythonRuffCheckExtraArgs>`
* new {ref}`${pythonRuffFixStamp}<pythonRuffFixStamp>` config item (used for **{ref}`py.fix<py.fix>`**) incremental build
* new config items fto list rules to be auto-fixed:
  * {ref}`${pythonAutoFixRules}<pythonAutoFixRules>` (list version)
  * {ref}`${pythonAutoFixJoinedRules}<pythonAutoFixJoinedRules>` (string version)

## Release 1.1.0

* new {ref}`${pythonEditableInstallArgs}<pythonEditableInstallArgs>` config item
* new {ref}`${pythonWheelInstallArgs}<pythonWheelInstallArgs>` config item
* changed **{ref}`py.install<py.install>`** and **{ref}`py.editable<py.editable>`** tasks pip install args to point to these new items
