from tkinter import ANCHOR, END, filedialog, DISABLED, NORMAL
from typing import List, Type, cast

import matplotlib.pyplot as plt
from analysis_tools.abstract_analysis_method import Analysis_Method_Protocol
from analysis_tools.analysis_method_options import Analysis_Method_Options
from analysis_tools.analysis_task import Analysis_Task
from models.analysis_results.abstract_analysis_result import Analysis_Result_Protocol
from models.image.analysis_images_model import Analysis_Images_Model
from views.analysis_settings_view import Analysis_Settings_View

from controller.abstract_controller import Main_Controller_Protocol


class Analysis_Settings_Controller:
    def __init__(
        self, parent_controller: Main_Controller_Protocol, images_model: Analysis_Images_Model
    ):
        """Controls the Analysis_Settings_View

        Args:
            parent_controller (Main_Controller_Protocol): The Main_Controller holding the GUI
            images_model (Images_Model): The model holding image data for later analysis
        """
        self.parent_controller: Main_Controller_Protocol = parent_controller
        self.images_model: Analysis_Images_Model = images_model
        self.view: Analysis_Settings_View = Analysis_Settings_View(
            parent_controller.view, images_model
        )

        self.preview_image_size = (self.view.image_canvas.winfo_width(), self.view.image_canvas.winfo_height())
        self.current_image = images_model.selected_image_as_ui_image(
            self.preview_image_size
        )

        self.selected_analysis_options: List[Analysis_Method_Options] = []

        self.setup_actions()

    def setup_actions(self):
        self.view.image_canvas.bind("<Configure>", self.resized_widget)

        self.view.image_canvas.create_image(0, 0, image=self.current_image, anchor="nw")

        self.view.next_button.configure(command=self.preview_next)
        self.view.prev_button.configure(command=self.preview_prev)

        self.view.add_analysis_button.configure(command=self.add_analysis_option)
        self.view.remove_analysis_button.configure(command=self.remove_analysis_option)
        self.view.run_analysis_button.configure(command=self.run_analysis, state=DISABLED)
        
        
    def add_analysis_option(self):
        option_value = self.view.analysis_options_dropdown_value.get()
        option = Analysis_Method_Options(option_value)
        if not option in self.selected_analysis_options:
            self.selected_analysis_options.append(option)
            self.view.selected_analysis_options_list.insert(END, option_value)
            self.view.run_analysis_button.configure(state=NORMAL)
        print("Analysis Options: ", self.selected_analysis_options)
        
    def remove_analysis_option(self):
        indices = self.view.selected_analysis_options_list.curselection()
        try:
            index = indices[0]
            print("Value to delete: ", index)
            del self.selected_analysis_options[index]
            self.view.selected_analysis_options_list.delete(ANCHOR)
            
            if len(self.selected_analysis_options) == 0:
                self.view.run_analysis_button.configure(state=DISABLED)

        except IndexError:
            print("No valid selection for element to delete.")
        
        

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

        self.analysis_task = Analysis_Task(self.view, self.process_analysis_results)

        for analysis_option in self.selected_analysis_options:
            try:
                method = cast(Type[Analysis_Method_Protocol], analysis_option.analysis_method())
                self.analysis_task.add_analysis_method(method)
            except:
                print("Error retrieving analysis method.")

        self.analysis_task.run_analysis(self.images_model.image_models)

        for child in self.view.winfo_children():
            child.destroy()

        self.view.create_progress_bar()

    def process_analysis_results(self, results: List[Analysis_Result_Protocol]):
        for result in results:
            result.save_results(self.output_dir_path)
            result.present_results()

        plt.show()

        self.selected_analysis_options.clear()
        
        for child in self.view.winfo_children():
            child.destroy()

        self.view.create_view(self.images_model)
        self.setup_actions()
