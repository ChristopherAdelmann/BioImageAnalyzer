from typing import Protocol, Tuple

from views.abstract_view import View


class Controller_Protocol(Protocol):
    def setup_actions(self):
        ...

    view: View


class Main_Controller_Protocol(Protocol):
    view: View

    def setup_actions(self):
        ...

    def resize_window(self, to_size: Tuple[int, int]):
        ...
