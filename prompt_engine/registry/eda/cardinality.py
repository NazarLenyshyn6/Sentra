""" ... """

from enum import Enum
from typing import Type, Dict
from typing_extensions import override

from ..base import PromptRegistry
from prompt_engine.components.eda import CardinalityComponent

class CardinalityPromptRegistry(PromptRegistry[CardinalityComponent]):
    """ ... """
    
    _registry: Dict[CardinalityComponent, str] = {}
    
    @override
    @classmethod
    def get_component_type(cls) -> Type[Enum]:
        return CardinalityComponent