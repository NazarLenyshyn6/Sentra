"""

This module defines the `TypeHandlingPromptRegistry`, a prompt registry specialized
for managing strategy-specific prompts related to data type handling within the EDA pipeline.

It extends the generic `PromptRegistry` base class by binding to the `TypeHandlingComponent` Enum,
which enumerates supported strategies for identifying, converting, and managing data types
(e.g., type inference, categorical encoding, type casting).

These prompts are used to dynamically guide code generation or agent behavior during 
the data type processing phase of exploratory data analysis.

"""

from enum import Enum
from typing import Type, Dict
from typing_extensions import override

from ..base import PromptRegistry
from prompt_engine.components.eda import TypeHandlingComponent

class TypeHandlingPromptRegistry(PromptRegistry[TypeHandlingComponent]):
    """
    Prompt registry for EDA strategies related to data type handling.

    This class binds the generic `PromptRegistry` to the `TypeHandlingComponent` Enum,
    enabling safe registration and retrieval of prompts for managing and converting data types.
    """
    
    _registry: Dict[TypeHandlingComponent, str] = {}
    
    @override
    @classmethod
    def get_component_type(cls) -> Type[Enum]:
        return TypeHandlingComponent
    
    
                                                                # Register Type Handling Prompts
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

TypeHandlingPromptRegistry.register_prompt(
    strategy=TypeHandlingComponent.CAST_MANUALLY,
    prompt="TypeHandling.CAST_MANUALLY: placeholder"
)

TypeHandlingPromptRegistry.register_prompt(
    strategy=TypeHandlingComponent.CLEAN_STRINGS,
    prompt="TypeHandling.CLEAN_STRINGS: placeholder"
)

TypeHandlingPromptRegistry.register_prompt(
    strategy=TypeHandlingComponent.CONVERT_OBJECT_TO_NUMERIC,
    prompt="TypeHandling.CONVERT_OBJECT_TO_NUMERIC: placeholder"
)

TypeHandlingPromptRegistry.register_prompt(
    strategy=TypeHandlingComponent.OPTIMIZE_CATEGORIES,
    prompt="TypeHandling.OPTIMIZE_CATEGORIES: placeholder"
)

TypeHandlingPromptRegistry.register_prompt(
    strategy=TypeHandlingComponent.INFER_TYPES,
    prompt="TypeHandling.INFER_TYPES: placeholder"
)

TypeHandlingPromptRegistry.register_prompt(
    strategy=TypeHandlingComponent.PARSE_DATETIME,
    prompt="TypeHandling.PARSE_DATETIME: placeholder"
)