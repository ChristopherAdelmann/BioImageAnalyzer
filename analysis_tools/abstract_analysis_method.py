
from typing import Protocol
from typing import List
from analysis_tools.threshold_options import Threshold_Options
from models.image.image_model import Image_Model
from models.analysis_results.abstract_analysis_result import Analysis_Result_Protocol

class Analysis_Method_Protocol(Protocol):
    @staticmethod
    def calculate(image_models: List[Image_Model], thresh_option: Threshold_Options = Threshold_Options.otsu) -> Analysis_Result_Protocol:
        ...