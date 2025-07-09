"""

This module defines enums that represent modular, executable strategies 
used during Exploratory Data Analysis (EDA). Each enum member corresponds 
to a specific component and maps to an instruction for generating Python code.

"""


from enum import Enum, auto


class DataIngestionComponent(Enum):
    """
    Supported data ingestion components.
    Each represents a method for loading structured data from a specific format.
    """
    
    CSV = auto()
    EXCEL = auto()
    PARQUET = auto()
    JSON = auto()
    
    
class MissingValuesComponent(Enum):
    """
    Strategies for handling missing values in a dataset.
    Each represents a common imputation or cleaning approach.
    """
    
    IMPUTE_MEAN = auto()
    IMPUTE_MEDIAN = auto()
    IMPUTE_MODE = auto()
    FILL_CONSTANT = auto()
    DROP_ROWS = auto()
    IMPUTE_KNN = auto()
    INTERPOLATE = auto()
    FORWARD_FILL = auto()
    BACKWARD_FILL = auto()
    
    
    
class TypeHandlingComponent(Enum):
    """
    Components for managing and transforming data types.
    Each represents a specific conversion or cleanup task.
    """
    
    INFER_TYPES = auto()
    CAST_MANUALLY = auto()
    OPTIMIZE_CATEGORIES = auto()
    PARSE_DATETIME = auto()
    CONVERT_OBJECT_TO_NUMERIC = auto()
    CLEAN_STRINGS = auto()
    
    
class UnivariativeAnalysisComponent(Enum):
    """
    Components for analyzing a single feature independently.
    Each represents a statistical or visual summary operation.
    """
    
    DESCRIPTIVE_STATS = auto()
    
    
class BivariativeAnalysisComponent(Enum):
    """
    Components for analyzing relationships between two features.
    Each represents a method for comparison, correlation, or aggregation.
    """
    
    ...
    

class OutlierDetectionComponent(Enum):
    """
    Strategies for detecting outliers in numerical features.
    Each represents a statistical or model-based approach.
    """
    
    Z_SCORE = auto()
    MODIFIED_Z_SCORE = auto()
    IQR = auto()
    ISOLATION_FOREST = auto()
    LOCAL_OUTLIER_FACTOR = auto()
    
    
class CardinalityComponent(Enum):
    """
    Components for analyzing feature cardinality and uniqueness.
    Each represents a strategy to assess or tag feature cardinality level.
    """
    
    UNIQUE_RATIO = auto()
    TAG_LOW_CARDINALITY = auto()
    TAG_HIGH_CARDINALITY = auto()
    DETECT_ID_LIKE_COLUMNS = auto()
    
    
class TargetAnalysisComponent(Enum):
    """
    Components for analyzing properties of the target variable.
    Each represents a method for distribution or relationship assessment.
    """
    
    CLASS_IMBALANCE = auto()
    TARGET_OUTLIERS = auto()
    FEATURE_TARGET_RELATIONSHIP = auto()
    BIN_TARGET_FOR_REGRESSION = auto()
    
    
    
class DataQualityComponent(Enum):
    """
    Strategies for identifying common data quality issues.
    Each represents a check or correction for data integrity.
    """
    
    DUPLICATE_ROWS = auto()
    INVALID_RANGES = auto()
    NULL_LIKE_VALUES = auto()
    

