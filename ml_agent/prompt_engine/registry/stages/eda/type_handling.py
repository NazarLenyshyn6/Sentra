"""
This module defines a reusable stage for data type handling.
It registers prompt-driven strategies to parse and convert data types for modeling compatibility.
"""

from prompt_engine.core.stage import Stage
from prompt_engine.registry.strategies.eda.type_handling import (
    ParseDatetime,
    ConvertObjectToNumeric
)

TypeHandlingStage = Stage(
    id = "type_handling",
    description="Use to convert or infer data types, ensuring compatibility with ML models."
    )

TypeHandlingStage.add_strategies(
    strategies=[
        ParseDatetime,
        ConvertObjectToNumeric
    ]
)