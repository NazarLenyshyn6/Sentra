"""

This module defines the `PromptTemplate` class, which coordinates the ordered execution
of prompt components defined by subclasses of `PromptRegistry`. Each component corresponds
to a stage in a pipeline (e.g., data ingestion, missing value handling, feature engineering),
and is responsible for managing prompts tied to specific strategies.

The `PromptTemplate` class provides an abstract, extensible template for generating
multi-step prompts by combining registered strategy-specific prompts in a defined order.

Design Goals:
- Maintain strict ordering of modular prompt components
- Enforce type-safe alignment between strategy and component
- Facilitate composable, explainable, step-based prompt generation
- Allow subclasses to define their own default component ordering

"""

from abc import ABC
from typing import List, Type
from enum import Enum

from prompt_engine.registry.base import PromptRegistry

ComponentsOrder = List[Type[PromptRegistry]]

class PromptTemplate(ABC):
    """
    Base class for managing the composition and ordering of multiple prompt components.

    Subclasses define the ordered list of prompt registries used to compose a complete
    multi-step prompt. Each registry corresponds to a component in the data pipeline and
    exposes strategy-specific prompt templates.

    This class provides validation to ensure the correctness and alignment between
    components and strategies, and supports fault-tolerant generation via `skip_missing`.
    """
    
    _components_order: ComponentsOrder = []
    
    def __init_subclass__(cls) -> None:
        """
        Ensures that subclasses explicitly define or initialize the `_components_order`.

        This safeguard prevents implicit inheritance of components order.
        
        Raises:
            AttributeError: If `_components_order` is not defined in the subclass.
        """
        super().__init_subclass__()
        if "_components_order" not in cls.__dict__:
            raise AttributeError(
                f"{cls.__name__} must define '_components_order'"
                )
        
    @classmethod
    def get_components_order(cls) -> ComponentsOrder:
        """
        Returns a copy of the currently configured prompt component order.

        This reflects the order in which individual prompts will be assembled
        in the final output string.

        Returns:
            ComponentsOrder: List of PromptRegistry subclasses in execution order.
        """
        return list(cls._components_order)
        
    @classmethod
    def get_prompt(cls, 
                   strategies: List[Enum], 
                   ) -> str:
        """
        Generates a composed, multi-step prompt from the configured components and strategies.

        Each component corresponds to a step, and the prompt for the corresponding strategy
        is fetched and appended

        Args:
            strategies: A list of Enum values corresponding to strategies
                                     for each registered component (must match order).

        Raises:
            ValueError: If the number of strategies does not match number of components,
                        or if a prompt is missing.
            TypeError: If any strategy does not match the expected Enum type of its component.
            
        Returns:
            str: The final composed multi-step prompt string.
        """
        prompt = []
        components = cls.get_components_order()
        
        if len(components) != len(strategies):
            raise ValueError(f"Expected {len(components)} strategies, got {len(strategies)}.")
        
        for component, strategy in zip(components, strategies):
            expected_enum = component.get_component_type()
            if not isinstance(strategy, expected_enum):
                raise TypeError(
                    f"{strategy} is unexpected strategy for {expected_enum.__name__}"
                )
            if not component.has_prompt(strategy):
                raise ValueError(
                    f"No prompt registered for strategy {strategy.name} in component {component.__name__}."
                )
            prompt.append(f"{component.get_prompt(strategy)}\n")
        
        return "\n\n".join(prompt)