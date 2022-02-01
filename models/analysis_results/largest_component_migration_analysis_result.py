from typing import List

import pandas as pd
from matplotlib_interface.multipage_image_fig import Multipage_Image_Fig
from models.image.image_model import Image_Model

from .abstract_analysis_result import Analysis_Result_Protocol


class Largest_Component_Migration_Analysis_Result(Analysis_Result_Protocol):
    def __init__(self, result_df: pd.DataFrame, result_image_models: List[Image_Model]):
        self.result_df = result_df
        self.result_image_models: List[Image_Model] = result_image_models

    def save_results(self, path: str):
        self.result_df.to_excel(f"{path}/{type(self).__name__}.xlsx")

    def present_results(self):
        self.image_fig = Multipage_Image_Fig(self.result_image_models, type(self).__name__)
        self.image_fig.setup()
