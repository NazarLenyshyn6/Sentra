"""
This module defines a set of reusable, prompt-driven strategies for handling missing values 
in tabular datasets. Each strategy represents a distinct method of imputation.
"""

from prompt_engine.core.strategy import Strategy


ImputeMean = Strategy(
    id="impute_mean",
    description="Use when missing values are numeric and approximately normally distributed.",
    prompt="."
)

ImputeMedian = Strategy(
    id="impute_median",
    description="Use when missing values are numeric and the feature contains outliers.",
    prompt="."
)

ImputeMode = Strategy(
    id="impute_mode",
    description="Use when the feature is categorical or has few unique values.",
    prompt="."
)

FillConstant = Strategy(
    id="fill_constant",
    description="Use when a specific placeholder or domain-specific value is needed.",
    prompt="."
)



    
