
from typing import List
import numpy as np
from PIL import Image

class Image_Paths_Model(object):
    def __init__(self) -> None:
        self.paths: List[str] = []
    
    def addPaths(self, new_paths: tuple[str]) -> None:
        self.paths += new_paths
        
    def getImages(self) -> List[np.ndarray]:
        images: List[np.ndarray] = []
        for path in self.paths:
            image = np.array(Image.open(path))
            print(image.shape)
            images.append(image)
        return images