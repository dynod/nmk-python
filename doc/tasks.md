# Tasks

The **`nmk-python`** plugin defines the tasks described below.

## Setup tasks

All tasks in this chapter are dependencies of the base [**`setup`**](https://nmk-base.readthedocs.io/en/stable/tasks.html#setup-task) task.

(py.version)=
### **`py.version`** -- Python version stamping

This task creates/updates the **{ref}`${pythonVersionStamp}<pythonVersionStamp>`** stamp file, only when [${gitVersion}](https://nmk-base.readthedocs.io/en/stable/config.html#gitversion-git-version) has changed. This allows incremental build depending on python version change (i.e. trigger rebuild if only version changed).

| Property | Value/description |
|-         |-
| builder  | {py:class}`nmk_python.version.PythonVersionRefresh`
| input    | [${gitVersionStamp}](https://nmk-base.readthedocs.io/en/stable/config.html#gitversionstamp-git-version-resolution-stamp-file) file
| output   | {ref}`${pythonVersionStamp}<pythonVersionStamp>` file
| if       | {ref}`${pythonSrcFiles}<pythonSrcFiles>` are found

The builder is called with the following parameters mapping:

| Name | Value |
|- |-
| version | **{ref}`${pythonVersion}<pythonVersion>`**

(py.project)=
### **`py.project`** -- Python project file generation

This task generates the **{ref}`${pythonProjectFile}<pythonProjectFile>`** project file.

| Property | Value/description |
|-         |-
| builder  | {py:class}`nmk_python.project.PythonProjectBuilder`
| input    | {ref}`${pythonProjectFileFragments}<pythonProjectFileFragments>` files
| output   | {ref}`${pythonProjectFile}<pythonProjectFile>` file
| if       | {ref}`${pythonSrcFiles}<pythonSrcFiles>` are found

The builder is called with the following parameters mapping:

| Name | Value |
|- |-
| fragment_files | **{ref}`${pythonProjectFileFragments}<pythonProjectFileFragments>`**
| items | **{ref}`${pythonProjectFileItems}<pythonProjectFileItems>`**

## Build tasks

All tasks in this chapter are dependencies of the base [**`build`**](https://nmk-base.readthedocs.io/en/stable/tasks.html#build-task) task.

(py.format)=
### **`py.format`** -- Python code format

This task calls **`ruff format`** command to format python code of this project.

| Property | Value/description |
|-         |-
| builder  | {py:class}`nmk_python.ruff.RuffBuilder`
| input    | {ref}`${pythonSrcFiles}<pythonSrcFiles>` + {ref}`${pythonProjectFile}<pythonProjectFile>` files
| output   | {ref}`${pythonRuffFormatStamp}<pythonRuffFormatStamp>` file
| if       | {ref}`${pythonSrcFiles}<pythonSrcFiles>` are found

The builder is called with the following parameters mapping:

| Name | Value |
|- |-
| src_folders | **{ref}`${pythonSrcFolders}<pythonSrcFolders>`**
| command | format

(py.analysis)=
### **`py.analysis`** -- Python code analysis

This task calls **`ruff check`** command to analyze python code of this project.

| Property | Value/description |
|-         |-
| builder  | {py:class}`nmk_python.ruff.RuffBuilder`
| input    | {ref}`${pythonSrcFiles}<pythonSrcFiles>` + {ref}`${pythonProjectFile}<pythonProjectFile>` files
| output   | {ref}`${pythonRuffCheckStamp}<pythonRuffCheckStamp>` file
| if       | {ref}`${pythonSrcFiles}<pythonSrcFiles>` are found

The builder is called with the following parameters mapping:

| Name | Value |
|- |-
| src_folders | **{ref}`${pythonSrcFolders}<pythonSrcFolders>`**
| command | check

## Build tasks

All tasks in this chapter are dependencies of the base [**`build`**](https://nmk-base.readthedocs.io/en/stable/tasks.html#build-task) task.

(py.build)=
### **`py.build`** -- Build Python wheel

This task use the python **`build`** module to handle the wheel build.

| Property | Value/description |
|-         |-
| builder  | {py:class}`nmk_python.build.PackageBuilder`
| input    | {ref}`${pythonSrcFiles}<pythonSrcFiles>` + {ref}`${pythonProjectFile}<pythonProjectFile>` files
| output   | {ref}`${pythonWheel}<pythonWheel>` file
| if       | {ref}`${pythonSrcFiles}<pythonSrcFiles>` are found

The builder is called with the following parameters mapping:

| Name | Value |
|- |-
| project_file | **{ref}`${pythonProjectFile}<pythonProjectFile>`**
| version_file | **{ref}`${pythonVersionStamp}<pythonVersionStamp>`**
| source_dirs | **{ref}`${pythonSrcFolders}<pythonSrcFolders>`**
| artifacts_dir | **{ref}`${pythonArtifacts}<pythonArtifacts>`**
| build_dir | **{ref}`${pythonBuildDir}<pythonBuildDir>`**

(py.install)=
### **`py.install`** -- Install Python wheel

This task installs the built python wheel in the project venv.

| Property | Value/description |
|-         |-
| builder  | {py:class}`nmk_python.build.Installer`
| input   | {ref}`${pythonWheel}<pythonWheel>` file
| output  | [${venvState}](https://nmk-base.readthedocs.io/en/stable/config.html#venvstate-output-requirements-file-name)
| if       | {ref}`${pythonSrcFiles}<pythonSrcFiles>` are found

The builder is called with the following parameters mapping:

| Name | Value |
|- |-
| name | **{ref}`${pythonPackage}<pythonPackage>`**
| pip_args | "--force-reinstall --no-deps ${venvPipArgs}"

## Tests tasks

All tasks in this chapter are dependencies of the base [**`tests`**](https://nmk-base.readthedocs.io/en/stable/tasks.html#tests-task) task.

(py.tests)=
### **`py.tests`** -- Run Python tests

This task calls **`pytest`** command to execute python tests.

| Property | Value/description |
|-         |-
| builder  | {py:class}`nmk_python.tests.PytestBuilder`
| if       | {ref}`${pythonTestSrcFiles}<pythonTestSrcFiles>` are found

The builder is called with the following parameters mapping:

| Name | Value |
|- |-
| pytest_args | **{ref}`${pytestExtraArgs}<pytestExtraArgs>`**
