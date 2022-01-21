from controller.abstract_controller import Main_Controller_Protocol
from models.image_paths_model import Image_Paths_Model
from views.file_picker_view import File_Picker_View
from tkinter import filedialog
from typing import cast



class File_Picker_Controller: 
    def __init__(self, parent_controller: Main_Controller_Protocol):
        self.parent_controller: Main_Controller_Protocol = parent_controller
        self.model: Image_Paths_Model = Image_Paths_Model()
        self.view: File_Picker_View = File_Picker_View(parent_controller.view)
        self.setup_actions()
        
    def __del__(self):
        print("Deinit")
        
    def setup_actions(self):
        self.view.buttons["browse_files"].configure(command=self.open_file_browser)
        
    def open_file_browser(self):
        from controller.main_controller import Main_Controller  
        filetypes = (
        ('TIFF images', '*.tif'),
        )
        
        file_paths = filedialog.askopenfilenames(initialdir = "/",
                                               title = "Select images",
                                               filetypes = filetypes )
        
        self.model.addPaths(cast(tuple[str], file_paths))
        
        parent_controller = cast(Main_Controller, self.parent_controller)
        
        parent_controller.finished_image_selection(self.model)