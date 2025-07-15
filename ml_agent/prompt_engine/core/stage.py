"""
This module defines the `Stage` class, which represents a distinct phase
within a machine learning pipeline. 

Each Stage holds a unique identifier, a human-readable description, and manages
a registry of prompt-driven strategies. These strategies encapsulate specific
logic or prompts related to the pipeline's stage and can be dynamically added,
removed, or queried.

The `Stage` class provides methods for summarizing its content, managing strategies,
and retrieving prompt snippets, supporting modular and flexible pipeline design.
"""


from typing import Dict, List
from dataclasses import dataclass, field

from pydantic import validate_call

from prompt_engine.core.strategy import Strategy
from prompt_engine.core.registry import Registry


@dataclass(slots=True)
class Stage(Registry[Strategy]):
    """
    Represents a pipeline stage containing multiple prompt-driven strategies.

    Attributes:
        id: Unique identifier for the stage, normalized to uppercase.
        description: A brief human-readable description of the stage.
        _registry: Internal mapping of strategy IDs to Strategy instances.

    The Stage class supports:
    - Adding or removing strategies dynamically.
    - Retrieving prompt snippets for registered strategies.
    - Providing concise summaries of the stage and its strategies.

    This design supports modularity and flexibility in ML pipelines where prompt
    generation or code generation strategies vary per stage.
    """
    
    id: str
    description: str = field(repr=False)
    _registry: Dict[str, Strategy] = field(default_factory=dict, repr=False)
    
    def get_usage_summary(self) -> str:
        """
        Return a concise one-line summary of the stage for quick reference.

        Returns:
            A formatted string combining the stage ID and description.
        """
        return f"{self.id:<20} : {self.description}"
    
    def get_strategies_summary(self) -> str:
        """
        Generate a multi-line summary listing all registered strategies within this stage.

        Returns:
            str: A formatted string showing the stage ID and an overview of all
            registered strategies by their usage summaries. If no strategies are
            registered, returns a message indicating that the stage has no strategies.
        """
        if len(self) == 0:
            return f"No strategies registered for stage '{self.id}'."
        lines = [f"\n Stage: {self.id}", "├── Strategies Overview:"]
        for strategy in self:
            lines.append(f"- {strategy.get_usage_summary()}")
        return '\n'.join(lines)
    
    @validate_call
    def add_strategies(self, strategies: List[Strategy]) -> None:
        """
        Add one or more strategies to this stage's registry.

        Each strategy is indexed by its unique ID (case-sensitive) within the registry.
        If a strategy with the same ID already exists, it will be overwritten.

        Args:
            strategies: A list of Strategy instances to register.

        Raises:
            ValidationError: If the input does not conform to List[Strategy].
        """
        for strategy in strategies:
            self._registry[strategy.id] = strategy
        
    @validate_call
    def remove_strategies(self, strategies: List[Strategy]) -> None:
        """
        Remove one or more strategies from this stage's registry.

        Strategies are removed by their IDs. If a given strategy ID is not present,
        it is silently ignored (no error raised).

        Args:
            strategies: A list of Strategy instances to remove.

        Raises:
            ValidationError: If the input does not conform to List[Strategy].
        """
        for strategy in strategies:
            self._registry.pop(strategy.id, None)
        
    @validate_call
    def get_prompt(self, strategy_id: str) -> str:
        """
        Retrieve the prompt snippet associated with a registered strategy.

        The lookup is case-insensitive with respect to the strategy ID.

        Args:
            strategy_id (str): The ID of the strategy to retrieve.

        Returns:
            str: The prompt snippet of the specified strategy.

        Raises:
            KeyError: If the strategy ID is not registered within this stage.
            ValidationError: If the input does not conform to str.
        """
        strategy_id = strategy_id.upper()
        if strategy_id not in self:
            raise KeyError(f"Strategy '{strategy_id}' not found in stage '{self.id}'.")
        prompt = self._registry[strategy_id].prompt
        return prompt
    
    def get_registry(self) -> Dict[str, Strategy]:
        """
        Retrieve a shallow copy of the internal strategies registry.

        This allows read-only access to the registered strategies without
        exposing the internal registry dictionary for direct modification.

        Returns:
            Dict[str, Strategy]: A dictionary mapping strategy IDs to their corresponding Strategy instances.
        """
        return dict(self._registry)
    
    
    