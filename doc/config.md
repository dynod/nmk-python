# Configuration Reference

The **`nmk-python`** plugin handles the configuration items listed in this page.

All of them are initiliazed with convenient default values, so that you don't need to setup them for a default working behavior. You can anyway override them in your project if you need to fine tune the plugin behavior. [Some items](extend.md) are specifically designed to be extended by **`nmk`** projects and plugins.

## Files

(pythonSrcFolders)=
### **`pythonSrcFolders`** -- Python source code folders

| Type | Default value |
|-     |-
| List[str]  | [ [${sourceDir}](https://nmk-base.readthedocs.io/en/stable/config.html#sourcedir-source-base-directory) ]

These are the paths **nmk** will browse to find source python files.

(pythonGeneratedSrcFiles)=
### **`pythonGeneratedSrcFiles`** -- Python generated source files

| Type | Default value |
|-     |-
| List[str]  | []

This is a list of generated source files, which shall be contributed by any source code generation logic (out of scope of this plugin).

(pythonFoundSrcFiles)=
### **`pythonFoundSrcFiles`** -- Python found source files

| Type | Default value |
|-     |-
| List[str]  | Generated by {py:class}`nmk_python.files.PythonFilesFinder`

This is the list of python files for this project (excluding test and generated ones;  found in **{ref}`${pythonSrcFolders}<pythonSrcFolders>`**).

(pythonTestSources)=
### **`pythonTestSources`** -- Python tests source code root folder

| Type | Default value |
|-     |-
| str  | [${sourceDir}](https://nmk-base.readthedocs.io/en/stable/config.html#sourcedir-source-base-directory)/tests

This is the root folder for python tests source code.

(pythonTestSrcFiles)=
### **`pythonTestSrcFiles`** -- Python tests found source files

| Type | Default value |
|-     |-
| List[str]  | Generated by {py:class}`nmk_python.files.PythonTestFilesFinder`

This is the list of python tests files for this project (found in **{ref}`${pythonTestSources}<pythonTestSources>`** folder).

(pythonSrcFiles)=
### **`pythonSrcFiles`** -- All python source files

| Type | Default value |
|-     |-
| List[str]  | [ **{ref}`${pythonFoundSrcFiles}<pythonFoundSrcFiles>`**, **{ref}`${pythonTestSrcFiles}<pythonTestSrcFiles>`**, **{ref}`${pythonGeneratedSrcFiles}<pythonGeneratedSrcFiles>`** ]

This is a concatenation of all python source code files for this project.

## Version

(pythonVersion)=
### **`pythonVersion`** -- Python version

| Type | Default value |
|-     |-
| str  | Generated by {py:class}`nmk_python.version.PythonVersionResolver`

This is the current project version (respecting [PyPa version specifiers](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-specifiers)), derived from [${gitVersion}](https://nmk-base.readthedocs.io/en/stable/config.html#gitversion-git-version)

(pythonVersionStamp)=
### **`pythonVersionStamp`** -- Python version stamp file

| Type | Default value |
|-     |-
| str  | [${outputDir}](https://nmk-base.readthedocs.io/en/stable/config.html#outputdir-output-base-directory)/.pythonversion

This is the python version stamp file, updated each time the version is modified.

(pythonMinVersion)=
### **`pythonMinVersion`** -- Minimum supported python version

| Type | Default value |
|-     |-
| str  | "3.8"

This is the minimum python version supported by this project.

(pythonMaxVersion)=
### **`pythonMaxVersion`** -- Maximum supported python version

| Type | Default value |
|-     |-
| str  | "3.12"

This is the maximum python version supported by this project.

(pythonSupportedVersions)=
### **`pythonSupportedVersions`** -- List of all supported python version

| Type | Default value |
|-     |-
| List[str]  | Generated by {py:class}`nmk_python.version.PythonSupportedVersionsResolver`

This is the list of all supported python versions for this project.

## Project

(pythonProjectFile)=
### **`pythonProjectFile`** -- Python project file

| Type | Default value |
|-     |-
| str  | ${PROJECTDIR}/pyproject.toml

This is python project file, holding settings for python package generation and various python tools.

(pythonProjectFileFragments)=
### **`pythonProjectFileFragments`** -- Python project contributed fragment files

| Type | Default value |
|-     |-
| List[str] | []

List of project fragment files to be merged in generated **{ref}`${pythonProjectFile}<pythonProjectFile>`** file.

(pythonProjectFileItems)=
### **`pythonProjectFileItems`** -- Python project file contributed items

| Type | Default value |
|-     |-
| Dict | {}

Dictionary of items to be contributed in generated **{ref}`${pythonProjectFile}<pythonProjectFile>`** file.

## Code format/analysis

(pythonLineLength)=
### **`pythonLineLength`** -- Max python source line length

| Type | Default value |
|-     |-
| int | 160

This is the maximum line length when formatting code with [ruff](https://astral.sh/ruff).

(pythonIgnoredRules)=
### **`pythonIgnoredRules`** -- List of ignored rules

| Type | Default value |
|-     |-
| List[str] | ["E203","E501"]

This is the list of rules that need to be ignored when analyzing code with [ruff](https://astral.sh/ruff).

(pythonRuffFormatStamp)=
### **`pythonRuffFormatStamp`** -- Python format stamp file

| Type | Default value |
|-     |-
| str | [${outputDir}](https://nmk-base.readthedocs.io/en/stable/config.html#outputdir-output-base-directory)/.ruff-format

This is the stamp file updated each time the **{ref}`py.format<py.format>`** task is executed.

(pythonRuffCheckStamp)=
### **`pythonRuffCheckStamp`** -- Python check stamp file

| Type | Default value |
|-     |-
| str | [${outputDir}](https://nmk-base.readthedocs.io/en/stable/config.html#outputdir-output-base-directory)/.ruff-check

This is the stamp file updated each time the **{ref}`py.analysis<py.analysis>`** task is executed.
