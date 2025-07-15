"""
This module defines the `Orchestrator` class, a centralized registry and controller
for managing the core components of an LLM-driven pipeline system.

The Orchestrator maintains registries for:
- Pipelines: Ordered workflows composed of stages.
- Stages: Discrete phases of processing within a pipeline.
- Strategies: Prompt-driven logic blocks for specific tasks.

It provides methods for registering, removing, and summarizing components, as well
as generating composed prompts based on selected strategies.

The Orchestrator is intended to provide global coordination and visibility across
the pipeline execution ecosystem.
"""

from typing import Dict, List

from pydantic import validate_call

from prompt_engine.core.pipeline import Pipeline
from prompt_engine.core.stage import Stage
from prompt_engine.core.strategy import Strategy

class Orchestrator:
    """
    Central coordinator for managing and accessing registered pipelines,
    stages, and strategies across the prompt-driven ML pipeline system.
    """
    
    _pipeline_registry: Dict[str, Pipeline] = {}
    _stage_registry: Dict[str, Stage] = {}
    _strategy_registry: Dict[str, Strategy] = {}
    
    
    @classmethod
    @validate_call
    def _add_strategies(cls, strategies: List[Strategy]) -> None:
        """
        Register a list of strategies to the internal strategy registry.

        Args:
            strategies (List[Strategy]): List of Strategy instances to register.
        """
        for strategy in strategies:
            cls._strategy_registry[strategy.id] = strategy
        
    @classmethod
    @validate_call
    def _remove_strategies(cls, strategies: List[Strategy]) -> None:
        """
        Remove a list of strategies from the internal strategy registry.

        Args:
            strategies (List[Strategy]): List of Strategy instances to remove.
        """
        for strategy in strategies:
            cls._strategy_registry.pop(strategy.id, None)
            
    @classmethod
    @validate_call
    def _add_stages(cls, stages: List[Stage]) -> None:
        """
        Register a list of stages and their strategies to the internal registries.

        Args:
            stages (List[Stage]): List of Stage instances to register.
        """
        for stage in stages:
            cls._stage_registry[stage.id] = stage
            strategies = [strategy for strategy in stage]
            cls._add_strategies(strategies)
        
    @classmethod
    @validate_call
    def _remove_stages(cls, stages: List[Stage]) -> None:
        """
        Remove a list of stages and their strategies from the internal registries.

        Args:
            stages (List[Stage]): List of Stage instances to remove.
        """
        for stage in stages:
            cls._stage_registry.pop(stage.id, None)
            strategies = [strategy for strategy in stage]
            cls._remove_strategies(strategies)
            
    @classmethod
    @validate_call
    def add_pipelines(cls, pipelines: List[Pipeline]) -> None:
        """
        Register a list of pipelines along with their associated stages and strategies.

        Args:
            pipelines (List[Pipeline]): List of Pipeline instances to register.
        """
        for pipeline in pipelines:
            cls._pipeline_registry[pipeline.id] = pipeline
            stages = [stage for stage in pipeline]
            cls._add_stages(stages)
        
    @classmethod
    def remove_pipelines(cls, pipelines: List[Pipeline]) -> None:
        """
        Remove a list of pipelines and their associated stages and strategies.

        Args:
            pipelines (List[Pipeline]): List of Pipeline instances to remove.
        """
        for pipeline in pipelines:
            cls._pipeline_registry.pop(pipeline.id, None)
            stages = [stage for stage in pipeline]
            cls._remove_stages(stages)
            
    @classmethod
    @validate_call
    def get_pipelines_usage_summary(cls) -> str:
        """
        Generate a usage summary for all registered pipelines.

        Returns:
            str: Concatenated string summaries for all pipelines.
        """
        return '\n'.join(
            pipeline.get_usage_summary() 
            for pipeline in cls._pipeline_registry.values()
            )
        
    @classmethod
    @validate_call
    def get_pipelines_stages_summary(cls, pipelines_id: List[str]) -> str:
        """
        Generate stage summaries for selected pipelines.

        Args:
            pipelines_id (List[str]): List of pipeline IDs to summarize.

        Returns:
            str: Concatenated string summaries for all stages within specified pipelines.

        Raises:
            KeyError: If any pipeline ID is not found in the registry.
        """
        pipelines = []
        for pipeline_id in pipelines_id:
            pipeline_id = pipeline_id.upper()
            if pipeline_id not in cls._pipeline_registry:
                raise KeyError(f"Pipeline with ID '{pipeline_id}' is not registered.")
            pipeline = cls._pipeline_registry[pipeline_id]
            pipelines.append(pipeline)
        return '\n'.join(
            pipeline.get_stages_summary()
            for pipeline in pipelines
        )
        
    @classmethod
    @validate_call
    def get_stages_strategies_summary(cls, stages_id: List[str]) -> str:
        """
        Generate strategy summaries for selected stages.

        Args:
            stages_id (List[str]): List of stage IDs to summarize.

        Returns:
            str: Concatenated string summaries for all strategies within specified stages.

        Raises:
            KeyError: If any stage ID is not found in the registry.
        """
        stages = []
        for stage_id in stages_id:
            stage_id = stage_id.upper()
            if stage_id not in cls._stage_registry:
                raise KeyError(f"Stage with ID '{stage_id}' is not registered.")
            stage = cls._stage_registry[stage_id]
            stages.append(stage)
        return '\n'.join(
            stage.get_strategies_summary()
            for stage in stages
        )
        
    @classmethod
    @validate_call
    def get_composed_prompt(cls, strategies_id: List[str]) -> str:
        """
        Compose a full prompt by joining prompt texts of selected strategies.

        Args:
            strategies (List[str]): List of strategy IDs whose prompts will be composed.

        Returns:
            str: Concatenated prompt text from the selected strategies.

        Raises:
            KeyError: If any strategy ID is not found in the registry.
        """
        prompt = []
        for strategy_id in strategies_id:
            strategy_id = strategy_id.upper()
            if strategy_id not in cls._strategy_registry:
                raise KeyError(f"Strategy with ID '{strategy_id}' is not registered.")
            prompt_component = cls._strategy_registry[strategy_id].prompt
            prompt.append(prompt_component)
        return '\n'.join(prompt)
    
    @classmethod
    def get_registry(cls) -> Dict[str, Dict]:
        """
        Retrieve the complete internal registry state.

        Returns:
            Dict[str, Dict]: A dictionary containing all registered components grouped by type:
                - "Pipelines": Mapping of pipeline ID to Pipeline instance.
                - "Stages": Mapping of stage ID to Stage instance.
                - "Strategies": Mapping of strategy ID to Strategy instance.
        """
        return {
            "Pipelines": dict(cls._pipeline_registry),
            "Stages": dict(cls._stage_registry),
            "Strategies": dict(cls._strategy_registry)
        }