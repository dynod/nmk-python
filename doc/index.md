# Documentation for nmk-python plugin

This plugin adds support for Python development in an **`nmk`** project:
* setup file generation
* code format with [black](https://github.com/psf/black)
* import sorting with [isort](https://github.com/PyCQA/isort)
* code analysis with [flake8](https://flake8.pycqa.org/)
* python wheel build
* test with [pytest](https://pytest.org)
* VSCode settings generation (if [**`nmk-vscode`**](https://github.com/dynod/nmk-vscode) plugin is also used)
* README badges generation (if [**`nmk-badges`**](https://github.com/dynod/nmk-badges) plugin is also used):
    * supported python versions
    * link to pypi.org
    * used tools
    * code coverage

```{toctree}
:caption: 'Contents'
:maxdepth: 2
usage
tasks
extend
config
contribs
```

## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
