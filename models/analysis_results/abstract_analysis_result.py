from abc import ABC
from typing import List, Protocol

import pandas as pd
from models.image.image_model import Image_Model


class Analysis_Result_Protocol(Protocol):
    result_df: pd.DataFrame
    result_image_models: List[Image_Model]

    def save_results(self, path: str):
        ...

    def present_results(self):
        ...
