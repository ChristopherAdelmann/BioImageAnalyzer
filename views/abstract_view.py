import tkinter as UI
from abc import abstractmethod
from tkinter.constants import BOTH, YES


class View(UI.Frame):
    @abstractmethod
    def create_view(self):
        raise NotImplementedError

    @classmethod
    def make_label(
        cls, frame: UI.Frame, row: int, col: int, sticky: str = "", **kwargs
    ) -> UI.Label:
        label = UI.Label(frame, **kwargs)
        label.grid(row=row, column=col, sticky=sticky)
        return label

    @classmethod
    def make_button(
        cls, frame: UI.Frame, row: int, col: int, sticky: str = "", **kwargs
    ) -> UI.Button:
        button = UI.Button(frame, **kwargs)
        button.grid(row=row, column=col, sticky=sticky)
        return button

    @classmethod
    def make_canvas(cls, frame: UI.Frame, row: int, col: int, **kwargs) -> UI.Canvas:
        canvas = UI.Canvas(frame, **kwargs)
        canvas.grid(row=row, column=col)
        return canvas
