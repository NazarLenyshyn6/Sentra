""" 

This module defines the `PromptComposer` class, 
a centralized utility to compose a unified prompt string by combining 
multiple individual prompts defined by various strategy enums.

`PromptComposer` manages the registration of prompt registries — each 
corresponding to a specific Enum-based strategy component — and provides 
a simple interface to retrieve and compose prompts for multiple strategies 
at once.

The main purpose is to allow clients to provide a list of strategy enum 
instances, and under the hood, `PromptComposer` automatically finds the 
corresponding prompt registries for each strategy’s Enum type, fetches 
their individual prompts, and concatenates them into a single composed prompt.

Key features:
- Register and unregister prompt registries mapped to Enum components.
- Validate input types to ensure only valid Enums and PromptRegistry subclasses are used.
- Retrieve a composed prompt string from a list of strategy enums with optional skipping of missing registries.
- Encapsulate registry management and prompt retrieval behind a simple interface.

This class abstracts away the complexity of managing multiple prompt 
registries and enables flexible, dynamic prompt composition for 
downstream code generation workflows.

"""

from enum import Enum
from typing import Type, List, Dict, Any
import inspect


from prompt_engine.components.eda import (
    DataIngestionComponent,
    MissingValuesComponent,
    TypeHandlingComponent,
    UnivariativeAnalysisComponent,
    BivariativeAnalysisComponent,
    OutliersDetectionComponent,
    CardinalityComponent,
    TargetAnalysisComponent,
    DataQualityComponent
    )
from prompt_engine.registry.eda.data_ingestion import DataIngestionPromptRegistry
from prompt_engine.registry.eda.missing_values import MissingValuesPromptRegistry
from prompt_engine.registry.eda.type_handling import TypeHandlingPromptRegistry
from prompt_engine.registry.eda.univariative_analysis import UnivariativeAnalysisPromptRegistry
from prompt_engine.registry.eda.bivariative_analysis import BivariativeAnalysisPromptRegistry
from prompt_engine.registry.eda.outliers_detection import OutliersDetectionPromptRegistry
from prompt_engine.registry.eda.cardinality import CardinalityPromptRegistry
from prompt_engine.registry.eda.target_analysis import TargetAnalysisPromptRegistry
from prompt_engine.registry.eda.data_quality import DataQualityPromptRegistry
from prompt_engine.registry.base import PromptRegistry



class PromptComposer:
    """    
    Compose unified prompt strings by combining prompts from multiple strategy enums.

    `PromptComposer` acts as a centralized manager for registering prompt 
    registries keyed by Enum components. Each registry stores instruction 
    templates (prompts) for specific strategy enums.

    Clients provide a list of strategy enum instances representing different 
    prompt components they want to include. `PromptComposer` automatically 
    locates the appropriate prompt registry for each strategy’s Enum type, 
    retrieves the individual prompt strings, and composes them into a 
    single concatenated prompt.

    This design abstracts away registry lookup and prompt retrieval details, 
    exposing a simple interface to generate complex, composed prompts from 
    modular, reusable components.
    """
    
    _component_registry_map: Dict[Type[Enum], Type[PromptRegistry]] = {}
    
    @classmethod
    def _validate_component(cls, component: Any) -> None:
        """
        Validate that the provided component is an Enum class.

        Args:
            component: The component to validate.

        Raises:
            TypeError: If the component is not a subclass of Enum.
        """
        if not inspect.isclass(component) or not issubclass(component, Enum):
            raise TypeError(f"Component must be an Enum class, got: {component}")
        
    @classmethod
    def _validate_registry(cls, registry: Any) -> None:
        """
        Validate that the provided registry is a subclass of PromptRegistry.

        Args:
            registry: The registry to validate.

        Raises:
            TypeError: If the registry is not a subclass of PromptRegistry.
        """
        if not inspect.isclass(registry) or not issubclass(registry, PromptRegistry):
            raise TypeError(f"Registry must be a subclass of PromptRegistry, got: {registry}")
        
    @classmethod
    def _get_registry(cls, component: Type[Enum]) -> Type[PromptRegistry]:
        """
        Retrieve the registered PromptRegistry for the given Enum component.

        Args:
            component: The Enum class representing the strategy component.

        Raises:
            TypeError: If the component is not a valid Enum class.
            KeyError: If no registry is registered for the component.
            
        Returns:
            Type[PromptRegistry]: The corresponding PromptRegistry class.
        """
        
        cls._validate_component(component)
        if component not in cls._component_registry_map:
            raise KeyError(
                f"No prompt registry registered for component: {component}"
                )
        return cls._component_registry_map[component]
    
    @classmethod
    def _get_prompt(cls, strategy: Enum) -> str:
        """
        Retrieve the prompt string corresponding to the given strategy enum instance.

        Args:
            strategy (Enum): An enum instance representing a specific strategy.

        Raises:
            KeyError: If no prompt registry is registered for the strategy's Enum type.
            
        Returns:
            str: The prompt string associated with the strategy.
        """
        registry = cls._get_registry(type(strategy))
        return registry.get_prompt(strategy)
    
    @classmethod
    def register_prompt_registry(
        cls, 
        component: Type[Enum],
        registry: Type[PromptRegistry],
        overwrite: bool = True
        ) -> None:
        """
        Register a PromptRegistry class for a specific Enum component.

        Args:
            component: The Enum class representing the strategy component.
            registry: The PromptRegistry subclass to register.
            overwrite: Whether to overwrite an existing registration. Defaults to True.

        Raises:
            TypeError: If component is not an Enum class or registry is not a subclass of PromptRegistry.
            ValueError: If a registry is already registered for the component and overwrite is False.
        """
        cls._validate_component(component)
        cls._validate_registry(registry)
        if not overwrite and component in cls._component_registry_map:
            raise ValueError(f"Registry already registered for component: {component}")
        cls._component_registry_map[component] = registry
        
    @classmethod
    def remove_prompt_registry(cls, component: Enum) -> None:
        """
        Unregister the prompt registry associated with the specified Enum component.

        Args:
            component: The Enum class whose registry should be removed.

        Raises:
            TypeError: If the component is not a valid Enum class.
        """
        cls._validate_component(component)
        if component in cls._component_registry_map: 
            cls._component_registry_map.pop(component)
        
    @classmethod
    def get_prompt(cls, strategies: List[Enum]) -> str:
        """
        Compose a single prompt string by concatenating prompts for the given strategy enums.

        Args:
            strategies (List[Enum]): A list of Enum instances representing the desired strategies.

        Raises:
            KeyError: If a registry is missing for any strategy's Enum type.
            
        Returns:
            str: The composed prompt string consisting of all individual prompts concatenated with newlines.
        """
        return '\n\n'.join(cls._get_prompt(strategy) for strategy in strategies)
    
    @classmethod
    def has_registry(cls, component: Type[Enum]) -> bool:
        """
        Check if a PromptRegistry is registered for the given Enum component.

        This method validates the input and returns a boolean indicating whether
        a prompt registry has been registered for the specified strategy component.

        Args:
            component: The Enum class representing the strategy component.

        Raises:
            TypeError: If the component is not a valid Enum class.

        Returns:
            bool: True if a registry is registered for the component, False otherwise.
        """
        cls._validate_component(component)
        return component in cls._component_registry_map
    
    
                                    # Register Prompt Registries
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PromptComposer.register_prompt_registry(
    component=DataIngestionComponent, 
    registry=DataIngestionPromptRegistry
    )

PromptComposer.register_prompt_registry(
    component=MissingValuesComponent, 
    registry=MissingValuesPromptRegistry
    )

PromptComposer.register_prompt_registry(
    component=TypeHandlingComponent, 
    registry=TypeHandlingPromptRegistry
    )

PromptComposer.register_prompt_registry(
    component=UnivariativeAnalysisComponent, 
    registry=UnivariativeAnalysisPromptRegistry
    )

PromptComposer.register_prompt_registry(
    component=BivariativeAnalysisComponent, 
    registry=BivariativeAnalysisPromptRegistry
    )

PromptComposer.register_prompt_registry(
    component=OutliersDetectionComponent, 
    registry=OutliersDetectionPromptRegistry
    )

PromptComposer.register_prompt_registry(
    component=CardinalityComponent, 
    registry=CardinalityPromptRegistry
    )

PromptComposer.register_prompt_registry(
    component=TargetAnalysisComponent, 
    registry=TargetAnalysisPromptRegistry
    )

PromptComposer.register_prompt_registry(
    component=DataQualityComponent, 
    registry=DataQualityPromptRegistry
    )