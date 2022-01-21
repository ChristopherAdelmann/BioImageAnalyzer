import tkinter as UI
from tkinter.constants import BOTH, NW, YES, S
from typing import Optional

import config as cfg
from models.images_model import Images_Model

from views.abstract_view import View


class Image_View(View):
    def __init__(self, parent_view: UI.Frame, images_model: Images_Model):
        super().__init__(parent_view, bg="blue")

        self.parent_view = parent_view
        self.images_model = images_model

        self.pack(expand=YES, fill=BOTH)

        self.image_label: UI.Label
        self.image_canvas: UI.Canvas

        self.create_view(images_model)


    def create_view(self, images_model: Images_Model):
        self.current_image = images_model.get_ui_image(
            0, (cfg.window_width, cfg.window_height)
        )

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.image_canvas = UI.Canvas(self, bg="yellow")
        self.image_canvas.grid(row=0, column=0, sticky="nsew")

        self.image_canvas.create_image(0, 0, image=self.current_image, anchor="nw")
        
        self.image_canvas.bind("<Configure>", self.resized_widget)

        # self.image_label = self.make_label(
        #     self, 0, 0, image=self.current_image, bg="green"
        # )

    def resized_widget(self, e):
        self.current_image = self.images_model.get_ui_image(0, (e.width, e.height))
        self.image_canvas.create_image(0, 0, image=self.current_image, anchor="nw")
