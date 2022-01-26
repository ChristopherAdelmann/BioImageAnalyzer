from enum import Enum
from typing import Type

from analysis_tools.cell_migration_analysis import Cell_Migration_Analysis
from .abstract_analysis_method import Analysis_Method

class Analysis_Option(Enum):
    none = 0
    cell_migration = 1
    
    def analysis_method(self) -> Type[Analysis_Method] | None:
        match self.value:
            case 1:
                return Cell_Migration_Analysis
            case _:
                return None