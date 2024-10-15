"""
Python project file builder
"""

from pathlib import Path
from typing import Any, List

from nmk_base.common import TemplateBuilder
from tomlkit import TOMLDocument, comment, loads
from tomlkit.toml_file import TOMLFile


class PythonProjectBuilder(TemplateBuilder):
    """
    Python project file builder
    """

    # Handle relative path for all contributions
    def _check_paths(self, value: Any):
        if isinstance(value, str):
            return self.relative_path(value)
        if isinstance(value, list):
            return list(map(self._check_paths, value))
        if isinstance(value, dict):
            return {k: self._check_paths(v) for k, v in value.items()}
        return value

    def _contribute(self, main: dict, update: dict):
        """
        Merge items from **update** dictionary into **main** one.
        Merge logic for existing items is:

        * for lists: new items are appended after existing ones
        * for dictionaries: existing dictionary is updated with new one content
        * for other types: existing values are replaces with new ones

        :param main: Settings dictionary to be updated
        :param update: Update dictionary to be merged into the existing one
        """

        for k, v in update.items():
            # Already exists in target model?
            if k in main:
                # List: extend
                if isinstance(v, list):
                    main[k].extend(self._check_paths(v))
                # Map: recursive contribution
                elif isinstance(v, dict):
                    self._contribute(main[k], v)
                # Otherwise: replace
                else:
                    main[k] = self._check_paths(v)
            else:
                # New key
                main[k] = self._check_paths(v)

    def build(self, fragment_files: List[str], items: dict):
        """
        Generates python project file from fragments and items

        :param fragment_files: List of fragment files to be merged
        :param items: Dict of project items to be merged
        """

        # Merge project fragments to generate final project
        project = {}
        for f_path in map(Path, fragment_files):
            try:
                # Update document with rendered template
                fragment_doc = loads(self.render_template(f_path, {}))
            except Exception as e:
                # Propagate error with file name
                raise ValueError(f"While loading project file template ({f_path}): {e}") from e
            self._contribute(project, fragment_doc.unwrap())

        # Iterate on items contributed through yml project files (only ones contributing maps)
        self._contribute(project, {k: v for k, v in items.items() if isinstance(v, dict)})

        # Finally write config to output file
        doc = TOMLDocument()
        doc.add(comment("Please don't edit: generated by nmk-python plugin"))
        doc.update(project)
        project_output = TOMLFile(self.main_output)
        project_output.write(doc)
