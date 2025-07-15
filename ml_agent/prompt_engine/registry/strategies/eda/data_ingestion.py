"""
This module defines a set of reusable, prompt-driven strategies for handling data ingestion.
Each strategy represents a distinct method of data ingestion.
"""

from prompt_engine.core.strategy import Strategy


CSV = Strategy(
    id="csv",
    description="Use for ingesting datasets in CSV format, commonly used for tabular data.",
    prompt="."
)

