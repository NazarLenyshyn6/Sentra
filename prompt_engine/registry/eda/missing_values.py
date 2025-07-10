"""

This module defines the `MissingValuesPromptRegistry`, a prompt registry specialized
for managing strategy-specific prompts related to the handling of missing values 
within the EDA pipeline.

It extends the generic `PromptRegistry` base class by binding to the `MissingValuesComponent` Enum,
which enumerates supported strategies for detecting, visualizing, and imputing missing data 
(e.g., null counts, heatmaps, mean/mode imputation, advanced fill methods).

These prompts are used to dynamically guide code generation or agent behavior during 
the missing value handling stage of exploratory data analysis.

"""

from enum import Enum
from typing import Type, Dict
from typing_extensions import override

from ..base import PromptRegistry
from prompt_engine.components.eda import MissingValuesComponent

class MissingValuesPromptRegistry(PromptRegistry[MissingValuesComponent]):
    """
    Prompt registry for EDA strategies related to missing value handling.

    This class binds the generic `PromptRegistry` to the `MissingValuesComponent` Enum,
    enabling safe registration and retrieval of prompts for detecting and imputing missing values 
    in datasets.
    """
    
    _registry: Dict[MissingValuesComponent, str] = {}
    
    @override
    @classmethod
    def get_component_type(cls) -> Type[Enum]:
        return MissingValuesComponent
    
    
    
                                                                # Register Missing Values Prompts
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

MissingValuesPromptRegistry.register_prompt(
    strategy=MissingValuesComponent.BACKWARD_FILL,
    prompt="MissingValues.BACKWARD_FILL: placeholder"
)

MissingValuesPromptRegistry.register_prompt(
    strategy=MissingValuesComponent.DROP_ROWS,
    prompt="MissingValues.DROP_ROWS: placeholder"
)

MissingValuesPromptRegistry.register_prompt(
    strategy=MissingValuesComponent.FILL_CONSTANT,
    prompt="MissingValues.FILL_CONSTANT: placeholder"
)

MissingValuesPromptRegistry.register_prompt(
    strategy=MissingValuesComponent.IMPUTE_KNN,
    prompt="MissingValues.IMPUTE_KNN: placeholder"
)

MissingValuesPromptRegistry.register_prompt(
    strategy=MissingValuesComponent.FORWARD_FILL,
    prompt="MissingValues.FORWARD_FILL: placeholder"
)

MissingValuesPromptRegistry.register_prompt(
    strategy=MissingValuesComponent.INTERPOLATE,
    prompt="MissingValues.INTERPOLATE: placeholder"
)

MissingValuesPromptRegistry.register_prompt(
    strategy=MissingValuesComponent.IMPUTE_MEAN,
    prompt="MissingValues.IMPUTE_MEAN: placeholder"
)

MissingValuesPromptRegistry.register_prompt(
    strategy=MissingValuesComponent.IMPUTE_MEDIAN,
    prompt="MissingValues.IMPUTE_MEDIAN: placeholder"
)

MissingValuesPromptRegistry.register_prompt(
    strategy=MissingValuesComponent.IMPUTE_MODE,
    prompt="MissingValues.IMPUTE_MODE: placeholder"
)