import tkinter as UI
from typing import Dict, Tuple, cast

from models.image_paths_model import Image_Paths_Model
from models.images_model import Images_Model
from views.main_view import Main_View

from controller.abstract_controller import Controller_Protocol
from controller.file_picker_controller import File_Picker_Controller
from controller.image_view_controller import Image_View_Controller


class Main_Controller:
    def __init__(self, root_view: UI.Tk) -> None:
        self.images_model: Images_Model = Images_Model()
        self.view: Main_View = Main_View(root_view)
        self.child_controller: Dict[str, Controller_Protocol] = {}
        self.setup_sub_controller()

    def setup_actions(self):
        pass

    def resize_window(self, to_size: Tuple[int, int]):
        self.view.resize_window(to_size)
        self.view.update()

    def setup_sub_controller(self):
        self.child_controller["file_picker"] = File_Picker_Controller(self)

    def finished_image_selection(self, image_paths_model: Image_Paths_Model):
        self.images_model.images_data += image_paths_model.getImages()
        controller: File_Picker_Controller = cast(
            File_Picker_Controller, self.child_controller["file_picker"]
        )
        controller.view.destroy()
        del self.child_controller["file_picker"]
        self.present_image_view()

    def present_image_view(self):
        window_height = round(self.view.winfo_screenheight() / 2)
        window_width = round(self.view.winfo_screenwidth() / 2)
        self.resize_window((window_width, window_height))
        self.child_controller["image_view"] = Image_View_Controller(
            self, self.images_model
        )
