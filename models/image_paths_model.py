from typing import List

import numpy as np
from PIL import Image

from models.base_image_model import Base_Image_Model


class Image_Paths_Model(object):
    def __init__(self) -> None:
        self.paths: List[str] = []

    def add_paths(self, new_paths: tuple[str]) -> None:
        self.paths += new_paths

    def get_image_models(self) -> List[Base_Image_Model]:
        image_models: List[Base_Image_Model] = []
        for path in self.paths:
            sub_image_models = self.create_image_models(path)
            image_models += sub_image_models

        return image_models

    def create_image_models(self, path: str) -> List[Base_Image_Model]:
        image = Image.open(path)
        
        shape = np.array(image).shape

        image_slices = image.n_frames
        
        print("Image_Slices with shape:", image_slices, shape)

        image_models: List[Base_Image_Model] = []

        for i in range(image_slices):
            image.seek(i)
            image_data = np.array(image)
            if i != 0:
                prev_image_data_shape = image_models[i -1].image_data.shape
                if prev_image_data_shape != image_data.shape:
                    image_models[i -1].total_slice_count = 1
                    break
                
            image_models.append(
                Base_Image_Model(path, image_data, i + 1, image_slices)
            )

        return image_models
