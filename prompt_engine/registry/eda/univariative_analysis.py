"""

This module defines the `UnivariativeAnalysisPromptRegistry`, a prompt registry specialized
for managing strategy-specific prompts related to the univariate analysis phase of the EDA pipeline.

It extends the generic `PromptRegistry` base class by binding to the `UnivariativeAnalysisComponent` Enum,
which enumerates supported strategies for analyzing individual variables
(e.g., distribution plotting, summary statistics, outlier detection on a single variable).

These prompts are used to dynamically guide code generation or agent behavior during the
univariate statistical exploration phase.

"""


from enum import Enum
from typing import Type, Dict
from typing_extensions import override

from ..base import PromptRegistry
from prompt_engine.components.eda import UnivariativeAnalysisComponent

class UnivariativeAnalysisPromptRegistry(PromptRegistry[UnivariativeAnalysisComponent]):
    """
    Prompt registry for EDA strategies related to univariate analysis.

    This class binds the generic `PromptRegistry` to the `UnivariativeAnalysisComponent` Enum,
    enabling safe registration and retrieval of prompts for analyzing individual features.
    """
    
    _registry: Dict[UnivariativeAnalysisComponent, str] = {}
    
    @override
    @classmethod
    def get_component_type(cls) -> Type[Enum]:
        return UnivariativeAnalysisComponent
    
    
    
                                                                # Register Univariative Analysis Prompts
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

UnivariativeAnalysisPromptRegistry.register_prompt(
    strategy=UnivariativeAnalysisComponent.DESCRIPTIVE_STATS,
    prompt="UnivariativeAnalysis.DESCRIPTIVE_STATS: placeholder"
)
