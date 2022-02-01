
from enum import Enum, auto

import numpy as np
import skimage.filters as filters


class Threshold_Options(Enum):
    otsu = 0
    triangle = 1
    yen = 2
    
    def thresh_value(self, image_data: np.ndarray) -> float:
        match self.value:
            case 0:
                return filters.threshold_otsu(image_data)
            case 1:
                return filters.threshold_triangle(image_data)
            case 2:
                return filters.threshold_yen(image_data)
            case _:
                return 0
