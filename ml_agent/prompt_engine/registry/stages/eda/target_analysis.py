"""
This module defines a reusable stage for target variable analysis.
It registers prompt-driven strategies to detect issues like class imbalance and target outliers.
"""

from prompt_engine.core.stage import Stage
from prompt_engine.registry.strategies.eda.target_analysis import (
    ClassImbalance,
    TargetOutliers
)

TargetAnalysisStage = Stage(
    id = "target_analysis",
    description="Use to assess the target variable for issues such as class imbalance or outlier targets, which affect modeling."
    )

TargetAnalysisStage.add_strategies(
    strategies=[
        ClassImbalance,
        TargetOutliers
    ]
)
