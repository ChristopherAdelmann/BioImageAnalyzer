
from typing import Protocol
from typing import List
from models.image.image_model import Image_Model

class Analysis_Method(Protocol):
    @staticmethod
    def calculate(image_models: List[Image_Model]):
        ...