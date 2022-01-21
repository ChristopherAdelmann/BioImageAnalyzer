from controller.abstract_controller import Main_Controller_Protocol
from models.images_model import Images_Model
from views.image_view import Image_View

class Image_View_Controller:
    def __init__(self, parent_controller: Main_Controller_Protocol, images_model: Images_Model):
        self.parent_controller: Main_Controller_Protocol = parent_controller
        self.images_model: Images_Model = images_model
        self.view: Image_View = Image_View(parent_controller.view, images_model)
        
    def setup_actions(self):
        pass
    
    