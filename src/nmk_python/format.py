import sys
from typing import List

from nmk_base.common import run_with_logs

from nmk.model.builder import NmkTaskBuilder


class BlackBuilder(NmkTaskBuilder):
    def build(self, src_folders: List[str], line_length: int):
        # Delegate to black
        run_with_logs([sys.executable, "-m", "black", "-l", str(line_length)] + src_folders, self.logger)

        # Touch output file
        self.main_output.touch()
