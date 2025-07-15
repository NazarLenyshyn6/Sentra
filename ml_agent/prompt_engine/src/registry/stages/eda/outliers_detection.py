"""
This module defines a reusable stage for outlier detection.
It registers prompt-driven strategies that identify anomalous data points using different methods.
"""

from prompt_engine.src.core.stage import Stage
from prompt_engine.src.registry.strategies.eda.outliers_detection import (
    ZScore,
    ModifiedZScore,
    IQR
)

OutliersDetectionStage = Stage(
    id = "outliers_detection",
    description="Use to detect anomalous values that may skew distributions, affect statistical inference, or harm model performance."
    )

OutliersDetectionStage.add_strategies(
    strategies=[
        ZScore,
        ModifiedZScore,
        IQR
        ]
    )


