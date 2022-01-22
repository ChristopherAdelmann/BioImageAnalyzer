from typing import List, Optional, Tuple, cast

from numpy import ndarray
from PIL import Image, ImageTk

from models.image_model import Image_Model


class Images_Model(object):
    def __init__(self, image_models: List[Image_Model] = []) -> None:
        self.image_models: List[Image_Model] = image_models

    def as_ui_image(
        self, index: int, output_size: Tuple[int, int]
    ) -> ImageTk.PhotoImage:
        selected_image_data: Optional[ndarray] = self.image_models[index].image_data
        selected_image: Image.Image = Image.fromarray(selected_image_data)

        x_scaling_factor = output_size[0] / selected_image.width
        y_scaling_factor = output_size[1] / selected_image.height

        scaling_factor = min(x_scaling_factor, y_scaling_factor)

        rescaled_image_size = tuple(
            round(s * scaling_factor) for s in selected_image.size
        )

        selected_image = selected_image.resize(rescaled_image_size, Image.ANTIALIAS)

        return ImageTk.PhotoImage(selected_image)
