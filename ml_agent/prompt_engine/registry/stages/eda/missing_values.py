"""
This module defines a reusable stage for handling missing values.
It registers prompt-driven strategies implementing various imputation techniques.
"""

from prompt_engine.core.stage import Stage
from prompt_engine.registry.strategies.eda.missing_values import (
    ImputeMean,
    ImputeMedian,
    ImputeMode,
    FillConstant
)

MissingValuesStage = Stage(
    id = "missing_values",
    description="Use to identify and impute missing values using statistical or domain-aware techniques."
    )

MissingValuesStage.add_strategies(
    strategies=[
        ImputeMean, 
        ImputeMedian, 
        ImputeMode, 
        FillConstant
        ]
    )