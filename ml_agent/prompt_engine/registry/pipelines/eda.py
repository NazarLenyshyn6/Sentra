"""
This module defines the `EdaPipeline`, which represents a structured sequence
of exploratory data analysis (EDA) stages for tabular datasets.

Each stage in the pipeline encapsulates a well-defined task such as handling
missing values or analyzing cardinality. Each task is supported by a set of
prompt-driven strategies designed to guide LLM-based code generation in a
modular and explainable way.

This structure allows for composable, transparent, and extensible EDA workflows
that can be dynamically adapted to user queries or dataset characteristics.
"""

from prompt_engine.core.pipeline import Pipeline
from prompt_engine.registry.stages.eda import (
    cardinality_analysis,
    data_ingestion,
    missing_values,
    outliers_detection,
    target_analysis,
    type_handling
)


EdaPipeline = Pipeline(
    id="eda",
    description="Use to perform structured exploratory data analysis (EDA) across key stages such as missing value handling, "
    "outlier detection, type normalization, and target analysis—enabling data quality assessment, model-readiness checks, "
    "and interpretable feature engineering."
    )

EdaPipeline.add_stages(
    stages=[
        cardinality_analysis.CardinalityAnalysisStage,
        missing_values.MissingValuesStage,
        outliers_detection.OutliersDetectionStage,
        target_analysis.TargetAnalysisStage,
        type_handling.TypeHandlingStage,
        data_ingestion.DataIngestionStage
        ]
)