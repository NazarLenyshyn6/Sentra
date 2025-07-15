"""
This module defines the `Pipeline` class, which represents a sequence of
stages in a machine learning or prompt-based automation system.

Each Pipeline contains a unique ID, a description, and a registry of stages,
where each stage encapsulates a set of strategies. The pipeline structure supports
modular design, introspection, and dynamic registration of components.
"""


from typing import Dict, List
from dataclasses import dataclass, field

from pydantic import validate_call

from prompt_engine.src.core.stage import Stage
from prompt_engine.src.core.registry import Registry


@dataclass(slots=True)
class Pipeline(Registry[Stage]):
    """
    Represents a pipeline composed of multiple stages, each responsible for
    a specific phase of an automated or ML-driven workflow.

    Attributes:
        id: Unique identifier for the pipeline, normalized to uppercase.
        description: A short explanation of the pipeline's purpose.
        _registry: Internal mapping of stage IDs to Stage instances.

    Provides utility methods for:
    - Registering and removing stages.
    - Querying registered stages.
    - Generating usage summaries for inspection or display.
    """
    
    id: str
    description: str = field(repr=False)
    _registry: Dict[str, Stage] = field(default_factory=dict, repr=False)
            
    def get_usage_summary(self) -> str:
        """
        Return a concise one-line summary of the pipeline for quick reference.

        Returns:
            A formatted string combining the pipeline ID and description.
        """
        return f"{self.id:<20} : {self.description}"
    
    def get_stages_summary(self) -> str:
        """
        Generate a multi-line summary listing all registered stages within this pipeline.

        Returns:
            str: A formatted string showing the pipeline ID and an overview of all
            registered stages by their usage summaries.If no stages are
            registered, returns a message indicating that the pipeline has no stages.
        """
        if len(self) == 0:
            return f"No stages registered for pipeline '{self.id}'."
        lines = [f"\n Pipeline: {self.id}", "├── Stages Overview:"]
        for stage in self:
            lines.append(f"- {stage.get_usage_summary()}")
        return '\n'.join(lines)
    
    @validate_call
    def add_stages(self, stages: List[Stage]) -> None:
        """
        Add one or more stages to the pipeline's registry.

        Each stage is registered using its unique ID (case-sensitive). If a stage
        with the same ID already exists, it will be overwritten.

        Args:
            stages: A list of Stage instances to register.

        Raises:
            ValidationError: If input does not conform to List[Stage].
        """
        for stage in stages:
            self._registry[stage.id] = stage
        
    @validate_call
    def remove_stages(self, stages: List[Stage]) -> None:
        """
        Remove one or more stages from the pipeline.

        Stages are removed based on their `id`. If a stage ID is not found,
        it is silently ignored.

        Args:
            stages: A list of Stage instances to remove.

        Raises:
            ValidationError: If input does not conform to List[Stage].
        """
        for stage in stages:
            self._registry.pop(stage.id, None)
        
    @validate_call
    def get_stage(self, stage_id: str) -> Stage:
        """
        Retrieve a registered stage by its ID.

        This method returns the `Stage` instance associated with the given ID.
        The lookup is case-insensitive (the ID is normalized to uppercase internally).

        Args:
            stage_id: The ID of the stage to retrieve (case-insensitive).

        Returns:
            The corresponding `Stage` instance registered under the provided ID.

        Raises:
            KeyError: If the stage ID is not found in the pipeline.
            ValidationError: If the input is not a string.
        """
        stage_id = stage_id.upper()
        if stage_id not in self:
            raise KeyError(f"Stage '{stage_id}' not found in pipeline '{self.id}'.")
        stage = self._registry[stage_id]
        return stage
    
    def get_registry(self) -> Dict[str, Stage]:
        """
        Retrieve a shallow copy of the internal stage registry.

        This allows external consumers to inspect the pipeline’s structure
        without directly modifying the internal registry.

        Returns:
            Dict[str, Stage]: A dictionary mapping stage IDs to Stage instances.
        """
        return dict(self._registry)
        