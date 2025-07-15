"""
This module defines a reusable stage for data ingestion.
It registers prompt-driven strategies that implement specific methods
for loading and parsing data from supported sources.
"""

from prompt_engine.core.stage import Stage
from prompt_engine.registry.strategies.eda.data_ingestion import (
    CSV,
)

DataIngestionStage = Stage(
    id = "data_ingestion",
    description="Use to load and parse data from supported sources."
    )

DataIngestionStage.add_strategies(strategies=[CSV])

