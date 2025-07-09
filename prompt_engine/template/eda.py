""" ... """


from prompt_engine.registry.eda.data_ingestion import DataIngestionPromptRegistry
from prompt_engine.registry.eda.type_handling import TypeHandlingPromptRegistry
from prompt_engine.registry.eda.missing_values import MissingValuesPromptRegistry
from prompt_engine.registry.eda.univariative_analysis import UnivariativeAnalysisPromptRegistry
from prompt_engine.registry.eda.data_quality import DataQualityPromptRegistry
from prompt_engine.registry.eda.target_analysis import TargetAnalysisPromptRegistry
from prompt_engine.registry.eda.bivariative_analysis import BivariativeAnalysisPromptRegistry
from prompt_engine.registry.eda.outlier_detection import OutlierDetectionPromptRegistry
from prompt_engine.registry.eda.cardinality import CardinalityPromptRegistry
from .base import (
    PromptTemplate, 
    ComponentsOrder
    )


class FullBasicEDAPipelineTemplate(PromptTemplate):
    """
    Template: Load data, infer types, handle missing values, describe features.
    Ideal starting point for most structured datasets.
    """
    _components_order: ComponentsOrder = [
        DataIngestionPromptRegistry,          # e.g., CSV, EXCEL
        TypeHandlingPromptRegistry,           # e.g., INFER_TYPES
        MissingValuesPromptRegistry,          # e.g., IMPUTE_MEAN, DROP_ROWS
        UnivariativeAnalysisPromptRegistry,   # e.g., DESCRIPTIVE_STATS
    ]


class RobustTypeCleaningTemplate(PromptTemplate):
    """
    Template: Deep type handling including manual casting and string cleanup.
    """
    _components_order: ComponentsOrder = [
        TypeHandlingPromptRegistry,           # e.g., INFER_TYPES
        TypeHandlingPromptRegistry,           # e.g., CONVERT_OBJECT_TO_NUMERIC
        TypeHandlingPromptRegistry,           # e.g., CLEAN_STRINGS
        TypeHandlingPromptRegistry,           # e.g., PARSE_DATETIME
        TypeHandlingPromptRegistry,           # e.g., OPTIMIZE_CATEGORIES
    ]


class AdvancedMissingValueImputationTemplate(PromptTemplate):
    """
    Template: Use advanced imputation strategies for complex missingness.
    """
    _components_order: ComponentsOrder = [
        MissingValuesPromptRegistry,          # e.g., FORWARD_FILL
        MissingValuesPromptRegistry,          # e.g., BACKWARD_FILL
        MissingValuesPromptRegistry,          # e.g., INTERPOLATE
        MissingValuesPromptRegistry,          # e.g., IMPUTE_KNN
    ]


class DataValidationAndCleaningTemplate(PromptTemplate):
    """
    Template: Detect quality issues and fix missing values.
    """
    _components_order: ComponentsOrder = [
        DataQualityPromptRegistry,            # e.g., DUPLICATE_ROWS
        DataQualityPromptRegistry,            # e.g., NULL_LIKE_VALUES
        DataQualityPromptRegistry,            # e.g., INVALID_RANGES
        MissingValuesPromptRegistry,          # e.g., IMPUTE_MODE
    ]


class OutlierDetectionAndCleanupTemplate(PromptTemplate):
    """
    Template: Detect outliers with multiple strategies and optionally remove/flag them.
    """
    _components_order: ComponentsOrder = [
        TypeHandlingPromptRegistry,           # ensure numeric before outlier detection
        OutlierDetectionPromptRegistry,       # e.g., Z_SCORE
        OutlierDetectionPromptRegistry,       # e.g., IQR
        OutlierDetectionPromptRegistry,       # e.g., ISOLATION_FOREST
    ]


class CardinalityAnalysisTemplate(PromptTemplate):
    """
    Template: Assess cardinality and tag problematic features.
    """
    _components_order: ComponentsOrder = [
        CardinalityPromptRegistry,            # e.g., UNIQUE_RATIO
        CardinalityPromptRegistry,            # e.g., TAG_LOW_CARDINALITY
        CardinalityPromptRegistry,            # e.g., TAG_HIGH_CARDINALITY
        CardinalityPromptRegistry,            # e.g., DETECT_ID_LIKE_COLUMNS
    ]


class TargetDistributionAndRelationshipTemplate(PromptTemplate):
    """
    Template: Analyze target distribution and relationship to features.
    """
    _components_order: ComponentsOrder = [
        TargetAnalysisPromptRegistry,         # e.g., CLASS_IMBALANCE
        TargetAnalysisPromptRegistry,         # e.g., TARGET_OUTLIERS
        TargetAnalysisPromptRegistry,         # e.g., FEATURE_TARGET_RELATIONSHIP
    ]


class VisualCorrelationAndInteractionTemplate(PromptTemplate):
    """
    Template: Explore univariate and bivariate relationships.
    """
    _components_order: ComponentsOrder = [
        UnivariativeAnalysisPromptRegistry,   # e.g., DESCRIPTIVE_STATS
        BivariativeAnalysisPromptRegistry,    # e.g., CORRELATION_MATRIX
        BivariativeAnalysisPromptRegistry,    # e.g., SCATTER_PLOTS
    ]


class FeatureEngineeringStarterTemplate(PromptTemplate):
    """
    Template: Start preparing features via type fixes, cardinality checks, outlier handling.
    """
    _components_order: ComponentsOrder = [
        TypeHandlingPromptRegistry,           # e.g., CONVERT_OBJECT_TO_NUMERIC
        CardinalityPromptRegistry,            # e.g., DETECT_ID_LIKE_COLUMNS
        OutlierDetectionPromptRegistry,       # e.g., Z_SCORE
    ]


class RegressionTargetBinningTemplate(PromptTemplate):
    """
    Template: Convert continuous target into bins for classification-style analysis.
    """
    _components_order: ComponentsOrder = [
        TargetAnalysisPromptRegistry,         # e.g., BIN_TARGET_FOR_REGRESSION
        UnivariativeAnalysisPromptRegistry,   # e.g., DESCRIPTIVE_STATS
        BivariativeAnalysisPromptRegistry,    # e.g., BOX_PLOTS_BY_CATEGORY
    ]


class MinimalQuickLookTemplate(PromptTemplate):
    """
    Template: Quick ingestion and numeric description for fast insights.
    """
    _components_order: ComponentsOrder = [
        DataIngestionPromptRegistry,          # e.g., CSV
        TypeHandlingPromptRegistry,           # e.g., INFER_TYPES
        UnivariativeAnalysisPromptRegistry,   # e.g., DESCRIPTIVE_STATS
    ]


class CleanAndDescribeTemplate(PromptTemplate):
    """
    Template: Clean data types and values, then describe numerics.
    """
    _components_order: ComponentsOrder = [
        TypeHandlingPromptRegistry,           # e.g., INFER_TYPES
        TypeHandlingPromptRegistry,           # e.g., CLEAN_STRINGS
        MissingValuesPromptRegistry,          # e.g., IMPUTE_MEDIAN
        UnivariativeAnalysisPromptRegistry,   # e.g., DESCRIPTIVE_STATS
    ]


class FullVisualEDAForModelingTemplate(PromptTemplate):
    """
    Template: Full pipeline before modeling — ingestion, cleanup, visual stats.
    """
    _components_order: ComponentsOrder = [
        DataIngestionPromptRegistry,
        TypeHandlingPromptRegistry,
        MissingValuesPromptRegistry,
        OutlierDetectionPromptRegistry,
        CardinalityPromptRegistry,
        UnivariativeAnalysisPromptRegistry,
        BivariativeAnalysisPromptRegistry,
        TargetAnalysisPromptRegistry,
    ]
