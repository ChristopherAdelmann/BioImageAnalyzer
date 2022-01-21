import tkinter as UI
from tkinter.constants import BOTH, YES

from views.abstract_view import View


class Main_View(View):
    def __init__(self, parent_view: UI.Tk) -> None:
        super().__init__(parent_view)

        self.parent_view = parent_view

        self.pack(expand=YES, fill=BOTH)

        self.create_view()

    def create_view(self):
        pass

    def resize_window(self, size: tuple[int, int]):
        self.parent_view.geometry(f"{size[0]}x{size[1]}")
        self.update()
