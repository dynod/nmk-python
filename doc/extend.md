# Configuration Extension

As for all **`nmk`** projects config items, [**`nmk-python`** ones](config.md) are all overridable by other plug-ins and project files. But the ones described on this page are specifically designed to be extended.

## Files

Python generated files list may be extended by plugins enabling such python code generation.

Following config items may be extended for that purpose:
* **{ref}`${pythonGeneratedSrcFiles}<pythonGeneratedSrcFiles>`**: List of python generated files.

  Example:
  ```yaml
  pythonGeneratedSrcFiles:
      - ${sourceDir}/some_generated_file.py
  ```

## Code format/analysis

Python code format/analysis behavior may be configured by python projects.

Following config items may be extended for that purpose:
* **{ref}`${pythonLineLength}<pythonLineLength>`**: python source code length

  Example:
  ```yaml
  pythonLineLength: 150
  ```
* **{ref}`${pythonIgnoredRules}<pythonIgnoredRules>`**: list of ignored rules

  Example:
  ```yaml
  pythonIgnoredRules:
    - E123
  ```

* **{ref}`${pythonAutoFixRules}<pythonAutoFixRules>`**: list of rules categories to auto-fix

  Example:
  ```yaml
  pythonAutoFixRules:
    - F401 # Auto-fix unused imports
  ```

## Build

Python wheel build behavior may be configured by python projects.

Following config items may be extended for that purpose:
* **{ref}`${pythonPackageRequirements}<pythonPackageRequirements>`** and **{ref}`${pythonPackageOptionalRequirements}<pythonPackageOptionalRequirements>`**: package mandatory/optional dependencies

  Example:
  ```yaml
  pythonPackageRequirements:
    - some-package-dep
  pythonPackageOptionalRequirements:
    option-name:
      - some-optional-dep
  ```
* **{ref}`${pythonProjectFileItems}<pythonProjectFileItems>`**: additional project configuration:
  * extra details on the project

    Example:
    ```yaml
    pythonProjectFileItems:
      project:
        description: Some descriptive text for my python package
    ```
* **{ref}`${pythonPackagePlatform}<pythonPackagePlatform>`**: package platform tag

  Example:
  ```yaml
  pythonPackagePlatform: win_amd64 # Windows 64bits specific package
  ```
* **{ref}`${pythonExtraResources}<pythonExtraResources>`**: extra resources to be bundled in the built wheel

  Example:
  ```yaml
  pythonExtraResources:
    out/somethingbuilt.lib: ${sourceDir}/my_package
  ```

## Tests

Python test behavior may be configured by python projects.

Following config items may be extended for that purpose:
* **{ref}`${pytestExtraArgs}<pytestExtraArgs>`**: pytest extra options

  Example:
  ```yaml
  pytestExtraArgs:
    cov-fail-under: 80
  ```
* **{ref}`${pythonProjectFileItems}<pythonProjectFileItems>`**: extra project config items to exclude folders from coverage

  Example:
  ```yaml
  pythonProjectFileItems:
    tool:
      coverage:
        run:
          omit:
            - src/some_package/templates/*
  ```
