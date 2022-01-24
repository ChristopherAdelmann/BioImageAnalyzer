from typing import Protocol

import pandas as pd


class Analysis_Result(Protocol):
    result_df: pd.DataFrame
