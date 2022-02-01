import tkinter as UI
from tkinter import ttk
from tkinter.constants import BOTH, HORIZONTAL, NW, YES, S

from analysis_tools.analysis_method_options import Analysis_Method_Options
from models.image.analysis_images_model import Analysis_Images_Model

from views.abstract_view import View


class Analysis_Settings_View(View):
    def __init__(self, parent_view: UI.Frame, images_model: Analysis_Images_Model):
        super().__init__(parent_view)

        self.parent_view = parent_view
        self.images_model = images_model

        self.pack(expand=YES, fill=BOTH)

        self.image_canvas: UI.Canvas
        self.settings_frame: UI.Frame

        self.create_view(images_model)

    def create_view(self, images_model: Analysis_Images_Model):

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.image_canvas = UI.Canvas(self)
        self.image_canvas.grid(row=0, column=0, sticky="nsew")

        self.settings_frame = UI.Frame(self)

        self.settings_frame.grid(row=0, column=1, sticky="n", padx=10)

        self.image_description_label = UI.Label(
            self.settings_frame, text=self.images_model.selected_image_description
        )
        self.image_description_label.grid(column=0, row=0, columnspan=2, sticky="w")

        self.prev_button = self.make_button(
            self.settings_frame, 1, 0, sticky="nsew", text="Prev"
        )
        self.next_button = self.make_button(
            self.settings_frame, 1, 1, sticky="nsew", text="Next"
        )

        self.analysis_options_dropdown_value = UI.StringVar(self)
        self.analysis_options_dropdown = ttk.OptionMenu(
            self.settings_frame,
            self.analysis_options_dropdown_value,
            Analysis_Method_Options.all_values()[0],
            *Analysis_Method_Options.all_values()
        )
        self.analysis_options_dropdown.grid(
            column=0, row=2, sticky="nsew", pady=(20, 5)
        )

        self.add_analysis_button = UI.Button(self.settings_frame, text="Add Analysis")
        self.add_analysis_button.grid(column=1, row=2, sticky="nsew", pady=(18, 7))

        self.selected_analysis_options_list = UI.Listbox(self.settings_frame)
        self.selected_analysis_options_list.grid(
            column=0, row=3, columnspan=2, sticky="nsew"
        )
        
        self.remove_analysis_button = UI.Button(self.settings_frame, text="Remove Analysis")
        self.remove_analysis_button.grid(column=0, row=4, columnspan=2, sticky="nsew", pady=(5, 20))

        self.run_analysis_button = UI.Button(self.settings_frame, text="Start Analysis")
        self.run_analysis_button.grid(column=0, row=5, columnspan=2, sticky="nsew")

        self.update()

    def create_progress_bar(self):
        self.progress_bar = ttk.Progressbar(
            self, orient=HORIZONTAL, length=300, mode="indeterminate"
        )
        self.progress_bar.pack(pady=20, padx=20, expand=True, fill=BOTH)
        self.progress_bar.start(5)
