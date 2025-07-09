""" 

This module defines the `DataIngestionPromptRegistry`, a prompt registry specialized
for managing strategy-specific prompts related to the data ingestion phase of the EDA pipeline.

It extends the generic `PromptRegistry` base class by binding to the `DataIngestionComponent` Enum,
which enumerates the supported ingestion strategies (e.g., file reading, schema detection, format inference).

These prompts are used to dynamically guide code generation or agent behavior during the data loading phase.

"""


from enum import Enum
from typing import Type, Dict
from typing_extensions import override


from ..base import PromptRegistry
from prompt_engine.components.eda import DataIngestionComponent


class DataIngestionPromptRegistry(PromptRegistry[DataIngestionComponent]):
    """ 
    Prompt registry for EDA strategies related to data ingestion.

    This class binds the generic `PromptRegistry` to the `DataIngestionComponent` Enum,
    enabling safe registration and retrieval of prompts for ingestion tasks. 
    """
    
    _registry: Dict[DataIngestionComponent, str] = {}
    
    @override
    @classmethod
    def get_component_type(cls) -> Type[Enum]:
        return DataIngestionComponent


                                                                # Register Data Ingestion Prompts
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

DataIngestionPromptRegistry.register_prompt(
    strategy=DataIngestionComponent.CSV,
    prompt="..."
)