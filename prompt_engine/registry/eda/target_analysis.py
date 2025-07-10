"""

This module defines the `TargetAnalysisPromptRegistry`, a prompt registry specialized
for managing strategy-specific prompts related to target variable analysis in the EDA pipeline.

It extends the generic `PromptRegistry` base class by binding to the `TargetAnalysisComponent` Enum,
which enumerates supported strategies for analyzing and understanding the target variable 
(e.g., distribution analysis, class balance checks, target transformations).

These prompts are used to dynamically guide code generation or agent behavior during 
the target exploration phase of exploratory data analysis.
    
"""


from enum import Enum
from typing import Type, Dict
from typing_extensions import override

from ..base import PromptRegistry
from prompt_engine.components.eda import TargetAnalysisComponent

class TargetAnalysisPromptRegistry(PromptRegistry[TargetAnalysisComponent]):
    """
    Prompt registry for EDA strategies related to target variable analysis.

    This class binds the generic `PromptRegistry` to the `TargetAnalysisComponent` Enum,
    enabling safe registration and retrieval of prompts for analyzing and preparing the target variable.
    """

    _registry: Dict[TargetAnalysisComponent, str] = {}
    
    @override
    @classmethod
    def get_component_type(cls) -> Type[Enum]:
        return TargetAnalysisComponent
    
    
                                                                # Register Target Analysis Prompts
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


TargetAnalysisPromptRegistry.register_prompt(
    strategy=TargetAnalysisComponent.BIN_TARGET_FOR_REGRESSION,
    prompt="TargetAnalysis.BIN_TARGET_FOR_REGRESSION: placeholder"
)

TargetAnalysisPromptRegistry.register_prompt(
    strategy=TargetAnalysisComponent.CLASS_IMBALANCE,
    prompt="TargetAnalysis.CLASS_IMBALANCE: placeholder"
)

TargetAnalysisPromptRegistry.register_prompt(
    strategy=TargetAnalysisComponent.FEATURE_TARGET_RELATIONSHIP,
    prompt="TargetAnalysis.FEATURE_TARGET_RELATIONSHIP: placeholder"
)

TargetAnalysisPromptRegistry.register_prompt(
    strategy=TargetAnalysisComponent.TARGET_OUTLIERS,
    prompt="TargetAnalysis.TARGET_OUTLIERS: placeholder"
)