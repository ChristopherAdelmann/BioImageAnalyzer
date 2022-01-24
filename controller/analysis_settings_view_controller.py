from tkinter import IntVar, filedialog

import config as cfg
import matplotlib.pyplot as plt
from analysis_tools.analysis_option import Analysis_Option
from analysis_tools.cell_isolation_analysis import Cell_Isolation_Analysis
from analysis_tools.cell_migration_analysis import Cell_Migration_Analysis
from matplotlib_interface.multipage_image_fig import Multipage_Image_Fig
from models.images_model import Images_Model
from views.analysis_settings_view import Analysis_Settings_View

from controller.abstract_controller import Main_Controller_Protocol


class Analysis_Settings_View_Controller:
    def __init__(
        self, parent_controller: Main_Controller_Protocol, images_model: Images_Model
    ):
        self.parent_controller: Main_Controller_Protocol = parent_controller
        self.images_model: Images_Model = images_model
        self.view: Analysis_Settings_View = Analysis_Settings_View(
            parent_controller.view, images_model
        )
        self.preview_image_size = (cfg.window_width, cfg.window_height)
        self.current_image = images_model.selected_image_as_ui_image(
            self.preview_image_size
        )

        self.cell_migration_analysis_enabled: IntVar = IntVar(
            self.view, value=Analysis_Option.none.value
        )

        self.setup_actions()

    def setup_actions(self):
        self.view.image_canvas.bind("<Configure>", self.resized_widget)

        self.view.image_canvas.create_image(0, 0, image=self.current_image, anchor="nw")

        self.view.next_button.configure(command=self.preview_next)
        self.view.prev_button.configure(command=self.preview_prev)

        self.view.cell_migration_analysis_checkbox.configure(
            variable=self.cell_migration_analysis_enabled
        )
        self.view.run_analysis_button.configure(command=self.run_analysis)

    def run_analysis(self):
        output_dir_path = filedialog.askdirectory(title="Output directory")
        print(self.cell_migration_analysis_enabled.get())
        self.view.update()
        if (
            Analysis_Option(self.cell_migration_analysis_enabled.get())
            == Analysis_Option.cell_migration
        ):
            cell_isolation_results = list(
                Cell_Isolation_Analysis.calculate(img)
                for img in self.images_model.image_models
            )
            cell_migration_result = Cell_Migration_Analysis.calculate(
                cell_isolation_results
            )

            cell_migration_result.result_df.to_excel(
                f"{output_dir_path}/cell_migration_analysis.xlsx"
            )

            migration_fig = Multipage_Image_Fig(
                cell_migration_result.result_image_models
            )
            migration_fig.setup()

        plt.show()

    def preview_next(self):
        self.images_model.image_index.next()
        self.view.image_description_label.configure(
            text=self.images_model.selected_image_description
        )
        self.current_image = self.images_model.selected_image_as_ui_image(
            self.preview_image_size
        )
        self.view.image_canvas.create_image(0, 0, image=self.current_image, anchor="nw")

    def preview_prev(self):
        self.images_model.image_index.prev()
        self.view.image_description_label.configure(
            text=self.images_model.selected_image_description
        )
        self.current_image = self.images_model.selected_image_as_ui_image(
            self.preview_image_size
        )
        self.view.image_canvas.create_image(0, 0, image=self.current_image, anchor="nw")

    def resized_widget(self, e):
        self.preview_image_size = (e.width, e.height)
        self.current_image = self.images_model.selected_image_as_ui_image(
            self.preview_image_size
        )
        self.view.image_canvas.create_image(0, 0, image=self.current_image, anchor="nw")
