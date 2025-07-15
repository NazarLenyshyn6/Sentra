"""
This module defines a reusable stage for cardinality analysis in data preprocessing.
It registers prompt-driven strategies that each implement a specific method
for analyzing feature cardinality.
"""

from prompt_engine.core.stage import Stage
from prompt_engine.registry.strategies.eda.cardinality_analysis import (
    UniqueRatio,
    TagLowCardinality
)

CardinalityAnalysisStage = Stage(
    id = "cardinality_analysis",
    description="Use to assess feature uniqueness and detect high/low cardinality, which impacts encoding and model interpretability."
    )

CardinalityAnalysisStage.add_strategies(
    strategies=[
        UniqueRatio,
        TagLowCardinality
        ]
    )