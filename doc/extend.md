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
