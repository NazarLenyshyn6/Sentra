"""
This module defines a set of reusable, prompt-driven strategies for handling cardinality analysis.
Each strategy represents a distinct method of cardinality analysis.
"""

from prompt_engine.core.strategy import Strategy


UniqueRatio = Strategy(
    id="unique_ratio",
    description="Use to identify features with a high or low ratio of unique values, "
                "indicating whether a feature is categorical or continuous.",
    prompt="."
)

TagLowCardinality = Strategy(
    id="tag_low_cardinality",
    description="Use to flag features with very few unique values for specialized encoding or aggregation.",
    prompt="."
)

