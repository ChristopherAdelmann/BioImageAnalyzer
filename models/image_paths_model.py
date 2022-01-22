from typing import List

import numpy as np
from PIL import Image
from models.image_model import Image_Model


class Image_Paths_Model(object):
    def __init__(self) -> None:
        self.paths: List[str] = []

    def addPaths(self, new_paths: tuple[str]) -> None:
        self.paths += new_paths

    def getImages(self) -> List[Image_Model]:
        images: List[Image_Model] = []
        for path in self.paths:
            image = Image_Model(path)
            images.append(image)
        return images
