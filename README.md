# nmk-python
Python plugin for nmk build system

<!-- NMK-BADGES-BEGIN -->
[![License: MIT License](https://img.shields.io/github/license/dynod/nmk-python)](https://github.com/dynod/nmk-python/blob/main/LICENSE)
[![Checks](https://img.shields.io/github/actions/workflow/status/dynod/nmk-python/build.yml?branch=main&label=build%20%26%20u.t.)](https://github.com/dynod/nmk-python/actions?query=branch%3Amain)
[![Issues](https://img.shields.io/github/issues-search/dynod/nmk?label=issues&query=is%3Aopen+is%3Aissue+label%3Aplugin%3Apython)](https://github.com/dynod/nmk/issues?q=is%3Aopen+is%3Aissue+label%3Aplugin%3Apython)
[![Supported python versions](https://img.shields.io/badge/python-3.9%20--%203.13-blue)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/nmk-python)](https://pypi.org/project/nmk-python/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://astral.sh/ruff)
[![Code coverage](https://img.shields.io/codecov/c/github/dynod/nmk-python)](https://app.codecov.io/gh/dynod/nmk-python)
[![Documentation Status](https://readthedocs.org/projects/nmk-python/badge/?version=stable)](https://nmk-python.readthedocs.io/)
<!-- NMK-BADGES-END -->

This plugin adds support for Python development in an **`nmk`** project:
* project file generation
* code format, fix and analysis with [ruff](https://astral.sh/ruff)
* python wheel build
* test with [pytest](https://pytest.org)
* VSCode settings generation (if [**`nmk-vscode`**](https://github.com/dynod/nmk-vscode) plugin is also used)
* README badges generation (if [**`nmk-badges`**](https://github.com/dynod/nmk-badges) plugin is also used):
    * supported python versions
    * link to pypi.org
    * used tools
    * code coverage

## Usage

To use this plugin in your **`nmk`** project, insert this reference:
```
refs:
    - pip://nmk-python!plugin.yml
```

## Documentation

This plugin documentation is available [here](https://nmk-python.readthedocs.io/)

## Issues

Issues for this plugin shall be reported on the [main  **`nmk`** project](https://github.com/dynod/nmk/issues), using the **plugin:python** label.
