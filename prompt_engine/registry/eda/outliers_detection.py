"""

This module defines the `OutliersDetectionPromptRegistry`, a prompt registry specialized
for managing strategy-specific prompts related to the outliers detection phase of the EDA pipeline.

It extends the generic `PromptRegistry` base class by binding to the `OutliersDetectionComponent` Enum,
which enumerates supported strategies for identifying and handling outlierss 
(e.g., statistical tests, visualization techniques, robust scaling).

These prompts are used to dynamically guide code generation or agent behavior during 
the outliers analysis and treatment stage of exploratory data analysis.

"""

from enum import Enum
from typing import Type, Dict
from typing_extensions import override

from ..base import PromptRegistry
from prompt_engine.components.eda import OutliersDetectionComponent

class OutliersDetectionPromptRegistry(PromptRegistry[OutliersDetectionComponent]):
    """
    Prompt registry for EDA strategies related to outliers detection.

    This class binds the generic `PromptRegistry` to the `OutliersDetectionComponent` Enum,
    enabling safe registration and retrieval of prompts for detecting and processing outlierss 
    in datasets.
    """
    
    _registry: Dict[OutliersDetectionComponent, str] = {}
    
    @override
    @classmethod
    def get_component_type(cls) -> Type[Enum]:
        return OutliersDetectionComponent
    
    
    
                                                                # Register Outliers Detection Prompts
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


OutliersDetectionPromptRegistry.register_prompt(
    strategy=OutliersDetectionComponent.IQR,
    prompt="OutliersDetection.IQR: placeholder"
)

OutliersDetectionPromptRegistry.register_prompt(
    strategy=OutliersDetectionComponent.ISOLATION_FOREST,
    prompt="OutliersDetection.ISOLATION_FOREST: placeholder"
)

OutliersDetectionPromptRegistry.register_prompt(
    strategy=OutliersDetectionComponent.LOCAL_OUTLIER_FACTOR,
    prompt="OutliersDetection.LOCAL_OUTLIERs_FACTOR: placeholder"
)

OutliersDetectionPromptRegistry.register_prompt(
    strategy=OutliersDetectionComponent.MODIFIED_Z_SCORE,
    prompt="OutliersDetection.MODIFIED_Z_SCORE: placeholder"
)

OutliersDetectionPromptRegistry.register_prompt(
    strategy=OutliersDetectionComponent.Z_SCORE,
    prompt="OutliersDetection.Z_SCORE: placeholder"
)