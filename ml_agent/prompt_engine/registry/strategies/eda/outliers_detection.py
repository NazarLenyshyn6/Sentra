"""
This module defines a set of reusable, prompt-driven strategies for handling outliers detection
in tabular datasets. Each strategy represents a distinct method of outliers detection.
"""

from prompt_engine.core.strategy import Strategy

ZScore = Strategy(
    id="z_score",
    description="Use to detect outliers in normally distributed data by measuring how many standard deviations a point is from the mean.",
    prompt="."
)

ModifiedZScore = Strategy(
    id="modified_z_score",
    description="Use to detect outliers in data with potential skew or non-normality, using median and MAD.",
    prompt="."
)

IQR = Strategy(
    id="iqr",
    description="Use to detect outliers based on the interquartile range, effective for skewed distributions.",
    prompt="."
)

