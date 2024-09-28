# Usage

To use this plugin in your **`nmk`** project, insert this reference in your **nmk.yml** main file:
```yaml
refs:
    - pip://nmk-python!plugin.yml
```

Then you can start adding python source files in your project **src** sub-folder.\
Once done, **`nmk`** build will:
* generate python settings files
* trigger code analysis and formatting tools
* build a python wheel integrating your code
