from pathlib import Path
from typing import List

from nmk.model.resolver import NmkListConfigResolver


class PythonFilesFinder(NmkListConfigResolver):
    def get_value(self, name: str) -> List[Path]:
        # Iterate on source paths, and find all python files
        return [
            src_file
            for src_path in map(Path, self.model.config["pythonSrcFolders"].value)
            for src_file in filter(lambda f: f.is_file(), src_path.rglob("*.py"))
        ]
