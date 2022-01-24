import tkinter as UI
from tkinter.constants import BOTH, YES
from typing import Dict

from views.abstract_view import View


class File_Picker_View(View):
    def __init__(self, parent_view: UI.Frame) -> None:
        super().__init__(parent_view)

        self.parent_view = parent_view

        self.labels: Dict[str, UI.Label] = {}
        self.buttons: Dict[str, UI.Button] = {}

        self.create_view()

    def create_view(self):
        self.pack(expand=YES, fill=BOTH, padx=20, pady=20)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.labels["description"] = self.make_label(
            self, 0, 0, text="Select one or multiple images to start.", sticky="e"
        )
        self.buttons["browse_files"] = self.make_button(
            self, 0, 1, text="Browse files", sticky="w"
        )
