import numpy as np
import pandas as pd

from models.abstract_analysis_result import Analysis_Result
from models.base_image_model import Result_Image_Model


class Cell_Isolation_Analysis_Result(Analysis_Result):
    def __init__(
        self,
        result_df: pd.DataFrame,
        result_image_model: Result_Image_Model,
        binary_image_mask: np.ndarray,
        labeled_image_data: np.ndarray,
    ):
        self.result_df = result_df
        self.result_image_model = result_image_model
        self.binary_image_mask = binary_image_mask
        self.labeled_image_data = labeled_image_data
