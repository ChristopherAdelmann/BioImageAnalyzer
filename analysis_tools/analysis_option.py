from enum import Enum

from models.abstract_analysis_result import Analysis_Result


class Analysis_Option(Enum):
    none = 0
    cell_migration = 1
    