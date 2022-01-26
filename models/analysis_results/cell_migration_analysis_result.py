from typing import List

import pandas as pd

from .abstract_analysis_result import Analysis_Result_Protocol
from models.image.image_model import Image_Model


class Cell_Migration_Analysis_Result(Analysis_Result_Protocol):
    def __init__(
        self, result_df: pd.DataFrame, result_image_models: List[Image_Model]
    ):
        self.result_df = result_df
        self.result_image_models: List[Image_Model] = result_image_models
