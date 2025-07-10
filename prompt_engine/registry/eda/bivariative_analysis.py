"""

This module defines the `BivariativeAnalysisPromptRegistry`, a prompt registry specialized
for managing strategy-specific prompts related to the bivariate analysis phase of the EDA pipeline.

It extends the generic `PromptRegistry` base class by binding to the `BivariativeAnalysisComponent` Enum,
which enumerates the supported strategies for analyzing relationships between two variables
(e.g., correlation analysis, scatter plot generation, pairwise distribution inspection).

These prompts are used to dynamically guide code generation or agent behavior during the
bivariate statistical exploration phase.

"""

from enum import Enum
from typing import Type, Dict
from typing_extensions import override

from ..base import PromptRegistry
from prompt_engine.components.eda import BivariativeAnalysisComponent


class BivariativeAnalysisPromptRegistry(PromptRegistry[BivariativeAnalysisComponent]):
    """
    Prompt registry for EDA strategies related to bivariate analysis.

    This class binds the generic `PromptRegistry` to the `BivariativeAnalysisComponent` Enum,
    enabling safe registration and retrieval of prompts for two-variable analytical tasks.
    """
    
    _registry: Dict[BivariativeAnalysisComponent, str] = {}
    
    @override
    @classmethod
    def get_component_type(cls) -> Type[Enum]:
        return BivariativeAnalysisComponent
    
                                                                # Register Bivariative Analysis Prompts
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

BivariativeAnalysisPromptRegistry.register_prompt(
    strategy=BivariativeAnalysisComponent.PLACEHOLDER,
    prompt="BivariativeAnalysis.PLACEHOLDER: placeholder"
)