import numpy as np
from PIL import Image
import ntpath


class Image_Model(object):
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.image_data = np.array(Image.open(image_path))
        self.file_name = ntpath.basename(image_path)