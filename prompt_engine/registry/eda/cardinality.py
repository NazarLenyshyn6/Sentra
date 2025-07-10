"""

This module defines the `CardinalityPromptRegistry`, a prompt registry specialized
for managing strategy-specific prompts related to the cardinality analysis phase of the EDA pipeline.

It extends the generic `PromptRegistry` base class by binding to the `CardinalityComponent` Enum,
which enumerates supported strategies for analyzing column cardinality 
(e.g., unique value counting, high-cardinality detection, low-variance filtering).

These prompts are used to dynamically guide code generation or agent behavior during 
the feature uniqueness and redundancy analysis phase.

"""

from enum import Enum
from typing import Type, Dict
from typing_extensions import override

from ..base import PromptRegistry
from prompt_engine.components.eda import CardinalityComponent

class CardinalityPromptRegistry(PromptRegistry[CardinalityComponent]):
    """
    Prompt registry for EDA strategies related to cardinality analysis.

    This class binds the generic `PromptRegistry` to the `CardinalityComponent` Enum,
    enabling safe registration and retrieval of prompts for analyzing feature uniqueness 
    and cardinality characteristics.
    """
    
    _registry: Dict[CardinalityComponent, str] = {}
    
    @override
    @classmethod
    def get_component_type(cls) -> Type[Enum]:
        return CardinalityComponent
    
    
                                                                # Register Cardinality Prompts
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

CardinalityPromptRegistry.register_prompt(
    strategy=CardinalityComponent.UNIQUE_RATIO,
    prompt="Cardinality.UNIQUE_RATIO placehodler"
)

CardinalityPromptRegistry.register_prompt(
    strategy=CardinalityComponent.TAG_LOW_CARDINALITY,
    prompt="Cardinality.TAG_LOW_CARDINALITY: placehodler"
)

CardinalityPromptRegistry.register_prompt(
    strategy=CardinalityComponent.TAG_HIGH_CARDINALITY,
    prompt="Cardinality.TAG_HIGH_CARDINALITY: placehodler"
)

CardinalityPromptRegistry.register_prompt(
    strategy=CardinalityComponent.DETECT_ID_LIKE_COLUMNS,
    prompt="Cardinality.DETECT_ID_LIKE_COLUMNS: placehodler"
)