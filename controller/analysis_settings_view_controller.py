import threading
from tkinter import IntVar, filedialog
from typing import Type, cast, List

import config as cfg
import matplotlib.pyplot as plt
from analysis_tools.abstract_analysis_method import Analysis_Method
from analysis_tools.analysis_option import Analysis_Option
from matplotlib_interface.multipage_image_fig import Multipage_Image_Fig
from models.analysis_results.abstract_analysis_result import Analysis_Result_Protocol
from models.analysis_results.cell_isolation_analysis_result import (
    Cell_Isolation_Analysis_Result,
)
from models.analysis_results.cell_migration_analysis_result import (
    Cell_Migration_Analysis_Result,
)
from models.analysis_task import Analysis_Task
from models.image.images_model import Images_Model
from views.analysis_settings_view import Analysis_Settings_View

from controller.abstract_controller import Main_Controller_Protocol


class Analysis_Settings_View_Controller:
    def __init__(
        self, parent_controller: Main_Controller_Protocol, images_model: Images_Model
    ):
        """Controls the Analysis_Settings_View

        Args:
            parent_controller (Main_Controller_Protocol): The Main_Controller holding the GUI
            images_model (Images_Model): The model holding image data for later analysis
        """
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

        self.analysis_result: Cell_Migration_Analysis_Result | None = None

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

    def run_analysis(self):
        """Starts the asynchronous image data analysis with the selected parameters"""
        self.output_dir_path = filedialog.askdirectory(title="Output directory")
        self.view.update()

        self.analysis_task = Analysis_Task(
            self.view, self.present_results, self.images_model.image_models
        )

        analysis_method = Analysis_Option(
            self.cell_migration_analysis_enabled.get()
        ).analysis_method()
        try:
            analysis_method = cast(Type[Analysis_Method], analysis_method)
            self.analysis_task.add_analysis_method(analysis_method)
        except:
            print("Is not a analysis method")

        self.analysis_task.run_analysis()

        for child in self.view.winfo_children():
            child.destroy()

        self.view.create_progress_bar()

    def process_analysis_results(self, future_analysis_result):
        """Callback function for the analysis result future completion

        Args:
            future_analysis_result (Future[Cell_Migration_Analysis_Result]): The completed future containing the analysis result
        """
        assert threading.current_thread() is threading.main_thread()
        self.analysis_result = future_analysis_result.result()
        self.analysis_result.result_df.to_excel(
            f"{self.output_dir_path}/cell_migration_analysis.xlsx"
        )

    def present_results(self, results: List[Analysis_Result_Protocol]):
        try:
            
            migration_fig = Multipage_Image_Fig(
                results[0].result_image_models
            )
            migration_fig.setup()
            plt.show()

            for child in self.view.winfo_children():
                child.destroy()

            self.analysis_result = None
            self.view.create_view(self.images_model)
            self.setup_actions()
        except:
            self.parent_controller.view.after(200, self.present_results)
