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
