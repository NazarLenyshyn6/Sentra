"""

This module defines the `PromptRegistry` base class, a generic, extensible interface for managing
instruction templates (prompts) that guide Python code generation based on task-specific strategies.

Each subclass corresponds to a specific component and uses its own Enum to identify strategy types. 
Prompts are stored as strings and indexed by Enum values.

Design Goals:
- Type-safe and Enum-driven strategy validation
- Separation of concerns through isolated registries per subclass
- Centralized management of prompt registration and retrieval
- Extensible for EDA, modeling, and other pipeline components

Intended Usage:
1. Define a strategy Enum for a specific component.
2. Create a subclass of `PromptRegistry` with its own `_registry` and Enum type.
3. Use class methods to register, retrieve, and remove prompts per strategy.

"""


from enum import Enum
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Dict, Any


T = TypeVar("T", bound=Enum)


class PromptRegistry(ABC, Generic[T]):
    """
    Base class for managing prompts tied to strategy enums.

    This abstract, generic class provides core functionality to register, retrieve, and delete
    prompts (instruction templates) that define how code should be generated for different strategies.

    Each subclass must:
    - Define its own `_registry` dictionary to avoid shared state
    - Implement `get_component_type()` to specify the Enum type representing valid strategies

    The base class ensures strategy type safety and enforces a consistent interface for all
    prompt registry components across the system.
    """
    
    _registry: Dict[T, str] = {}
    
    def __init_subclass__(cls) -> None:
        """
        Enforces that each subclass defines its own `_registry`.

        This prevents subclasses from accidentally sharing the same prompt storage.

        Raises:
            KeyError: If `_registry` is not defined in the subclass.
        """
        super().__init_subclass__()
        if "_registry" not in cls.__dict__:
            raise AttributeError(
                f"{cls.__name__} must define its own class-level '_registry' to isolate prompt storage."
            )
        
    @classmethod
    def _validate_strategy(cls, strategy: Any) -> None:
        """
        Validates that the provided strategy is of the expected Enum type.

        Args:
            strategy: The strategy to validate.

        Raises:
            TypeError: If the strategy is not an instance of the subclass's Enum.
        """
        component_type = cls.get_component_type()
        if not isinstance(strategy, component_type):
            raise TypeError(
                f"Invalid strategy type: expected instance of {component_type.__name__}, "
                f"got {type(strategy).__name__}."
            )
                    
    @classmethod
    def register_prompt(cls, strategy: T, prompt: str, overwrite: bool = True) -> None:
        """
        Registers a prompt for the specified strategy.

        If the strategy already exists, the prompt will be overwritten.

        Args:
            strategy: The strategy Enum value to associate with the prompt.
            prompt: The prompt string (instruction/template for code generation).
            
        Raises:
            TypeError: If the strategy is not an instance of the subclass's Enum.
        """
        cls._validate_strategy(strategy)
        if not overwrite and strategy in cls._registry:
            raise KeyError(
                f"Prompt already registered for {strategy.name}. Use overwrite=True to replace it."
                )
        cls._registry[strategy] = prompt
        
    @classmethod
    def remove_prompt(cls, strategy: T) -> None:
        """
        Removes the prompt associated with the given strategy.

        Args:
            strategy: The strategy Enum value to remove.
            
        Raises:
            TypeError: If the strategy is not an instance of the subclass's Enum.
        """
        cls._validate_strategy(strategy)
        if strategy in cls._registry:
            cls._registry.pop(strategy)
        
    @classmethod
    def get_prompt(cls, strategy: T) -> str:
        """
        Retrieves the prompt for the specified strategy.

        Args:
            strategy: The strategy Enum value whose prompt is requested.

        Returns:
            str: The prompt string associated with the strategy.

        Raises:
            TypeError: If the strategy is not an instance of the subclass's Enum.
            KeyError: If no prompt is registered under the given strategy.
        """
        cls._validate_strategy(strategy)
        if strategy not in cls._registry:
            raise KeyError(
                f"No prompt registered for strategy: {strategy.name} ({strategy}). "
                f"Use `register_prompt()` to add it first."
                )
        return cls._registry[strategy]
    
    @classmethod
    def get_all_prompts(cls) -> Dict[T, str]:
        """
        Returns a copy of all registered prompts for this component.

        Useful for inspection, debugging, and dynamic agent behavior.

        Returns:
            Dict[T, str]: A dictionary mapping strategies to their associated prompts.
        """
        return dict(cls._registry)
    
    @classmethod
    def has_prompt(cls, strategy: T) -> bool:
        """
        Checks whether a prompt is registered for the given strategy.

        Args:
            strategy (T): The strategy Enum value to check.

        Returns:
            bool: True if a prompt is registered; False otherwise.
        
        Raises:
            TypeError: If the strategy is not an instance of the expected Enum.
        """
        cls._validate_strategy(strategy)
        return strategy in cls._registry
            
    @classmethod
    @abstractmethod
    def get_component_type(cls) -> Type[Enum]:
        """
        Specifies the Enum type used to validate strategy keys.

        Subclasses must implement this to indicate which Enum their `_registry` uses.

        Returns:
            Type[Enum]: The Enum class used to index strategies.
        """
        ...