import numpy as np
import pandas as pd

from models.abstract_analysis_result import Analysis_Result
from models.base_image_model import Result_Image_Model
from typing import List


class Cell_Migration_Analysis_Result(Analysis_Result):
    def __init__(self, result_df: pd.DataFrame, result_image_models: List[Result_Image_Model]):
        self.result_df = result_df
        self.result_image_models: List[Result_Image_Model] = result_image_models
