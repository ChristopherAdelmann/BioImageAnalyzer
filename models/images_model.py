from typing import List, Optional, Tuple, cast
from PIL import Image, ImageTk
from numpy import ndarray


class Images_Model(object):
    
    def __init__(self) -> None:
        self.images_data: List[ndarray] = []
        
    def get_ui_image(self, index: int, output_size: Tuple[int, int]) -> ImageTk.PhotoImage:
        selected_image_data: Optional[ndarray] = self.images_data[index]
        selected_image: Image.Image = Image.fromarray(selected_image_data)
        
        x_scaling_factor = output_size[0] / selected_image.width
        y_scaling_factor = output_size[1] / selected_image.height
        
        scaling_factor = min(x_scaling_factor, y_scaling_factor)
                
        rescaled_image_size = tuple(round(s * scaling_factor) for s in selected_image.size)
        
        selected_image = selected_image.resize(rescaled_image_size, Image.ANTIALIAS)
        
        return ImageTk.PhotoImage(selected_image)
        