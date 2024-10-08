"""
Python project file builder
"""

from pathlib import Path
from typing import List

from nmk_base.common import TemplateBuilder
from tomlkit import TOMLDocument, comment, loads
from tomlkit.toml_file import TOMLFile


class PythonProjectBuilder(TemplateBuilder):
    """
    Python project file builder
    """

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
                    main[k].extend(v)
                # Map: recursive contribution
                elif isinstance(v, dict):
                    self._contribute(main[k], v)
                # Otherwise: replace
                else:
                    main[k] = v
            else:
                # New key
                main[k] = v

    def build(self, fragment_files: List[str], items: dict):
        """
        Generates python project file from fragments and items

        :param fragment_files: List of fragment files to be merged
        :param items: Dict of project items to be merged
        """

        # Merge project fragments to generate final project
        project = {}
        for f_path in map(Path, fragment_files):
            # Update document with rendered template
            fragment_doc = loads(self.render_template(f_path, {}))
            self._contribute(project, fragment_doc.unwrap())

        # Iterate on items contributed through yml project files (only ones contributing maps)
        self._contribute(project, {k: v for k, v in items.items() if isinstance(v, dict)})

        # Finally write config to output file
        doc = TOMLDocument()
        doc.add(comment("Please don't edit: generated by nmk-python plugin"))
        doc.update(project)
        project_output = TOMLFile(self.main_output)
        project_output.write(doc)
