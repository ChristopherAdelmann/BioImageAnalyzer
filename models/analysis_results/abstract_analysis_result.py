from abc import ABC
from typing import Protocol

import pandas as pd


class Analysis_Result_Protocol(Protocol):
    result_df: pd.DataFrame
