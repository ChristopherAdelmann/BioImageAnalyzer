from typing import List
from enum import Enum
from typing import Type
from analysis_tools.largest_component_isolation_analysis_method import Largest_Component_Isolation_Analysis

from analysis_tools.largest_component_migration_analysis_method import Largest_Component_Migration_Analysis
from analysis_tools.largest_component_roughness_analysis_method import Largest_Component_Roughness_Analysis

from .abstract_analysis_method import Analysis_Method_Protocol


class Analysis_Method_Options(Enum):
    largest_component_analysis = "Largest Component Isolation"
    migration_analysis = "Largest Component Migration"
    roughness_analysis = "Largest Component Roughness"
    
    
    def analysis_method(self) -> Type[Analysis_Method_Protocol] | None:
        match self:
            case Analysis_Method_Options.largest_component_analysis:
                return Largest_Component_Isolation_Analysis
            case Analysis_Method_Options.migration_analysis:
                return Largest_Component_Migration_Analysis
            case Analysis_Method_Options.roughness_analysis:
                return Largest_Component_Roughness_Analysis

    @staticmethod
    def all_values() -> List[str]:
        values = [e.value for e in Analysis_Method_Options]
        return values