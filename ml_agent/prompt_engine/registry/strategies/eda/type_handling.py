"""
This module defines a set of reusable, prompt-driven strategies for handling type_handling
in tabular datasets. Each strategy represents a distinct method of type_handling.
"""

from prompt_engine.core.strategy import Strategy


ParseDatetime = Strategy(
    id="parse_datetime",
    description="Use to convert columns containing date or time information into datetime objects for easier analysis.",
    prompt="."
)

ConvertObjectToNumeric = Strategy(
    id="convert_object_to_numeric",
    description="Use to convert object-type columns containing numeric values into proper numeric dtype.",
    prompt="."
)



