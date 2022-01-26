from typing import List
import numpy as np
import pandas as pd

from .abstract_analysis_result import Analysis_Result_Protocol
from models.image.image_model import Image_Model

class Cell_Isolation_Analysis_Result(Analysis_Result_Protocol):
    def __init__(
        self,
        result_df: pd.DataFrame,
        result_image_models: List[Image_Model],
        labeled_image_models: List[Image_Model],
    ):
        self.result_df = result_df
        self.result_image_models = result_image_models
        self.labeled_image_models = labeled_image_models
