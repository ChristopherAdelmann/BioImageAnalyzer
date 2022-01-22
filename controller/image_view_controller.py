from models.cell_area_analysis import Cell_Area_Analysis
from models.images_model import Images_Model
from views.image_view import Image_View

from controller.abstract_controller import Main_Controller_Protocol


class Image_View_Controller:
    def __init__(
        self, parent_controller: Main_Controller_Protocol, images_model: Images_Model
    ):
        self.parent_controller: Main_Controller_Protocol = parent_controller
        self.images_model: Images_Model = images_model
        self.view: Image_View = Image_View(parent_controller.view, images_model)

        Cell_Area_Analysis.calculate(images_model.image_models)

    def setup_actions(self):
        pass
