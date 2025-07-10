"""

This module defines the `DataQualityPromptRegistry`, a prompt registry specialized
for managing strategy-specific prompts related to the data quality assessment phase of the EDA pipeline.

It extends the generic `PromptRegistry` base class by binding to the `DataQualityComponent` Enum,
which enumerates supported strategies for detecting and addressing data quality issues 
(e.g., missing values, duplicates, outliers, and inconsistent formats).

These prompts are used to dynamically guide code generation or agent behavior during 
the data validation and cleaning stages of exploratory data analysis.

"""

from enum import Enum
from typing import Type, Dict
from typing_extensions import override

from ..base import PromptRegistry
from prompt_engine.components.eda import DataQualityComponent

class DataQualityPromptRegistry(PromptRegistry[DataQualityComponent]):
    """
    Prompt registry for EDA strategies related to data quality assessment.

    This class binds the generic `PromptRegistry` to the `DataQualityComponent` Enum,
    enabling safe registration and retrieval of prompts for identifying and resolving 
    data quality issues.
    """
    
    _registry: Dict[DataQualityComponent, str] = {}
    
    @override
    @classmethod
    def get_component_type(cls) -> Type[Enum]:
        return DataQualityComponent
    
    
                                                                # Register Data Quality Prompts
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

DataQualityPromptRegistry.register_prompt(
    strategy=DataQualityComponent.DUPLICATE_ROWS,
    prompt="DataQuality.DUPLICATE_ROWS: placeholder"
)

DataQualityPromptRegistry.register_prompt(
    strategy=DataQualityComponent.INVALID_RANGES,
    prompt="DataQuality.INVALID_RANGES: placeholder"
)

DataQualityPromptRegistry.register_prompt(
    strategy=DataQualityComponent.NULL_LIKE_VALUES,
    prompt="DataQuality.NULL_LIKE_VALUES: placeholder"
)