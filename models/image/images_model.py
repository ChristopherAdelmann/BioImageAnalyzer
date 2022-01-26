from typing import List, Optional, Tuple, cast

import numpy as np
from PIL import Image, ImageTk
from skimage import exposure, img_as_ubyte

from .image_model import Image_Model
from .image_index import Image_Index


class Images_Model(object):
    def __init__(self, image_models: List[Image_Model] = []) -> None:
        self.image_models: List[Image_Model] = image_models
        self.image_index = Image_Index(len(image_models) - 1)
        
    def selected_image_model(self) -> Image_Model:
        return self.image_models[self.image_index.index]
    
    @property
    def selected_image_description(self):
        return f"Image {self.image_index.index + 1} of {self.image_index.max_index + 1}: {self.selected_image_model().image_description}"

    def selected_image_as_ui_image(
        self, output_size: Tuple[int, int]
    ) -> ImageTk.PhotoImage:
        return self.as_ui_image(self.image_index.index, output_size)

    def as_ui_image(
        self, index: int, output_size: Tuple[int, int]
    ) -> ImageTk.PhotoImage:
        selected_image_data: Optional[np.ndarray] = self.image_models[index].image_data
        uint8_image_data = img_as_ubyte(exposure.rescale_intensity(selected_image_data))
        selected_image: Image.Image = Image.fromarray(uint8_image_data)

        x_scaling_factor = output_size[0] / selected_image.width
        y_scaling_factor = output_size[1] / selected_image.height

        scaling_factor = min(x_scaling_factor, y_scaling_factor)

        rescaled_image_size = tuple(
            round(s * scaling_factor) for s in selected_image.size
        )

        selected_image = selected_image.resize(rescaled_image_size, Image.ANTIALIAS)

        return ImageTk.PhotoImage(selected_image)
