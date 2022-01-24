import tkinter as UI
from tkinter.constants import BOTH, NW, YES, S

from analysis_tools.analysis_option import Analysis_Option
from models.images_model import Images_Model

from views.abstract_view import View


class Analysis_Settings_View(View):
    def __init__(self, parent_view: UI.Frame, images_model: Images_Model):
        super().__init__(parent_view)

        self.parent_view = parent_view
        self.images_model = images_model

        self.pack(expand=YES, fill=BOTH)

        self.image_canvas: UI.Canvas
        self.settings_frame = UI.Frame

        self.create_view(images_model)

    def create_view(self, images_model: Images_Model):

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.image_canvas = UI.Canvas(self)
        self.image_canvas.grid(row=0, column=0, sticky="nsew")

        self.settings_frame = UI.Frame(self)

        self.settings_frame.grid(row=0, column=1, sticky="n")

        self.prev_button = self.make_button(
            self.settings_frame, 0, 0, sticky="nsew", text="Prev"
        )
        self.next_button = self.make_button(
            self.settings_frame, 0, 1, sticky="nsew", text="Next"
        )

        self.image_description_label = UI.Label(
            self.settings_frame, text=self.images_model.selected_image_description
        )
        self.image_description_label.grid(column=0, row=1, columnspan=2, sticky="w")

        self.cell_migration_analysis_checkbox = UI.Checkbutton(
            self.settings_frame,
            text="Cell migration analysis",
            offvalue=Analysis_Option.none.value,
            onvalue=Analysis_Option.cell_migration.value,
        )
        self.cell_migration_analysis_checkbox.grid(
            column=0, row=2, columnspan=2, sticky="w", pady=(20, 5)
        )

        self.run_analysis_button = UI.Button(self.settings_frame, text="Analyze")
        self.run_analysis_button.grid(column=0, row=3, columnspan=2, sticky="nsew")
