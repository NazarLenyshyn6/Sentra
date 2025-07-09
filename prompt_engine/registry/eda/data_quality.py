""" ... """

from enum import Enum
from typing import Type, Dict
from typing_extensions import override

from ..base import PromptRegistry
from prompt_engine.components.eda import DataQualityComponent

class DataQualityPromptRegistry(PromptRegistry[DataQualityComponent]):
    """ ... """
    
    _registry: Dict[DataQualityComponent, str] = {}
    
    @override
    @classmethod
    def get_component_type(cls) -> Type[Enum]:
        return DataQualityComponent