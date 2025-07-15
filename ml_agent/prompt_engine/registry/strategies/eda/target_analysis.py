"""
This module defines a set of reusable, prompt-driven strategies for handling target analysis
in tabular datasets. Each strategy represents a distinct method of target analysis.
"""

from prompt_engine.core.strategy import Strategy

ClassImbalance = Strategy(
    id="class_imbalance",
    description="Use to assess if the target variable has uneven class distributions that may impact model performance.",
    prompt="..."
)

TargetOutliers = Strategy(
    id="target_outliers",
    description="Use to detect abnormal or extreme target values that could bias model training.",
    prompt="..."
)



