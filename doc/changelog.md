# Changelog

Here are listed all the meaningfull changes done on **`nmk-python`** since version 1.0

```{note}
Only interface and important behavior changes are listed here.

The fully detailed changelog is also available on [Github](https://github.com/dynod/nmk-python/releases)
```

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
