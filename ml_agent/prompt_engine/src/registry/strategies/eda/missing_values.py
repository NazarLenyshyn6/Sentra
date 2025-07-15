"""
This module defines a set of reusable, prompt-driven strategies for handling missing values 
in tabular datasets. Each strategy represents a distinct method of imputation.
"""

from prompt_engine.src.core.strategy import Strategy


ImputeMean = Strategy(
    id="impute_mean",
    description="Use when missing values are numeric and approximately normally distributed.",
    prompt="""
You are tasked with imputing missing values using the mean strategy for numeric features that are approximately normally distributed.

## Task Description:
Replace missing values in numeric columns with the mean of the non-missing values, suitable for normally distributed data.

## When to Use:
- Numeric features with approximately normal distribution
- When outliers are minimal or have been handled
- For features where mean represents a reasonable central tendency
- When maintaining the original distribution shape is important

## Implementation Steps:

1. **Validate Data Type**:
   ```python
   if not pd.api.types.is_numeric_dtype(df[column]):
       raise ValueError(f"Column {column} is not numeric")
   ```

2. **Check Distribution**:
   - Calculate skewness to verify near-normal distribution
   - Use Shapiro-Wilk test for normality (if sample size < 5000)
   - Visualize distribution with histogram and Q-Q plot

3. **Calculate Mean**:
   - Compute mean excluding missing values
   - Handle edge cases (all values missing, single value)
   - Store original statistics for documentation

4. **Output Requirements**:
   - Return DataFrame with imputed values
   - Include imputation metadata: original_missing_count, imputed_value, column_mean, column_std
   - Generate before/after comparison plots
   - Report imputation summary statistics

5. **Special Considerations**:
   - Warn if skewness > 1 or < -1 (not normally distributed)
   - Handle infinite values before imputation
   - Preserve original data types
   - Consider impact on correlation with other features

## Expected Python Code Structure:
```python
def impute_mean(df, column):
    import pandas as pd
    import numpy as np
    from scipy import stats
    
    # Validate numeric column
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column {column} is not numeric")
    
    # Check for missing values
    missing_count = df[column].isnull().sum()
    if missing_count == 0:
        return df, {'imputed_count': 0, 'method': 'mean'}
    
    # Calculate mean excluding missing values
    mean_value = df[column].mean()
    
    # Check distribution (warn if not normal)
    skewness = df[column].skew()
    if abs(skewness) > 1:
        print(f"Warning: Column {column} has skewness {skewness:.2f}, may not be normally distributed")
    
    # Perform imputation
    df_imputed = df.copy()
    df_imputed[column] = df_imputed[column].fillna(mean_value)
    
    # Prepare metadata
    metadata = {
        'column': column,
        'method': 'mean',
        'imputed_count': missing_count,
        'imputed_value': mean_value,
        'original_mean': mean_value,
        'original_std': df[column].std(),
        'skewness': skewness
    }
    
    return df_imputed, metadata
```

Generate complete, executable Python code that implements this mean imputation strategy.
"""
)

ImputeMedian = Strategy(
    id="impute_median",
    description="Use when missing values are numeric and the feature contains outliers.",
    prompt="""
You are tasked with imputing missing values using the median strategy for numeric features that contain outliers or are skewed.

## Task Description:
Replace missing values in numeric columns with the median of the non-missing values, robust to outliers and skewed distributions.

## When to Use:
- Numeric features with outliers present
- Skewed distributions (non-normal)
- When mean would be heavily influenced by extreme values
- For robust imputation that preserves distribution characteristics

## Implementation Steps:

1. **Validate Data Type**:
   ```python
   if not pd.api.types.is_numeric_dtype(df[column]):
       raise ValueError(f"Column {column} is not numeric")
   ```

2. **Assess Skewness and Outliers**:
   - Calculate skewness to confirm non-normal distribution
   - Identify outliers using IQR method
   - Compare mean vs median to assess impact of outliers

3. **Calculate Median**:
   - Compute median excluding missing values
   - Handle edge cases (all values missing, single value)
   - Store original statistics for documentation

4. **Output Requirements**:
   - Return DataFrame with imputed values
   - Include imputation metadata: original_missing_count, imputed_value, median_value, mean_value, skewness
   - Generate before/after comparison plots
   - Report outlier statistics

5. **Special Considerations**:
   - Highlight difference between mean and median
   - Identify and count outliers before imputation
   - Preserve original data types
   - Consider impact on distribution shape

## Expected Python Code Structure:
```python
def impute_median(df, column):
    import pandas as pd
    import numpy as np
    
    # Validate numeric column
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column {column} is not numeric")
    
    # Check for missing values
    missing_count = df[column].isnull().sum()
    if missing_count == 0:
        return df, {'imputed_count': 0, 'method': 'median'}
    
    # Calculate statistics
    median_value = df[column].median()
    mean_value = df[column].mean()
    skewness = df[column].skew()
    
    # Identify outliers using IQR method
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR))]
    outlier_count = len(outliers)
    
    # Perform imputation
    df_imputed = df.copy()
    df_imputed[column] = df_imputed[column].fillna(median_value)
    
    # Prepare metadata
    metadata = {
        'column': column,
        'method': 'median',
        'imputed_count': missing_count,
        'imputed_value': median_value,
        'original_median': median_value,
        'original_mean': mean_value,
        'skewness': skewness,
        'outlier_count': outlier_count,
        'mean_median_diff': abs(mean_value - median_value)
    }
    
    return df_imputed, metadata
```

Generate complete, executable Python code that implements this median imputation strategy.
"""
)

ImputeMode = Strategy(
    id="impute_mode",
    description="Use when the feature is categorical or has few unique values.",
    prompt="""
You are tasked with imputing missing values using the mode strategy for categorical features or features with few unique values.

## Task Description:
Replace missing values with the most frequently occurring value (mode) in categorical or low-cardinality features.

## When to Use:
- Categorical features (string, object, category dtypes)
- Numeric features with few unique values
- When the most common value is a reasonable replacement
- For preserving the original distribution of categories

## Implementation Steps:

1. **Validate Feature Type**:
   ```python
   is_categorical = df[column].dtype in ['object', 'category'] or df[column].nunique() < 10
   ```

2. **Calculate Mode**:
   - Find the most frequent value excluding missing values
   - Handle ties (multiple modes) by selecting first occurrence
   - Handle edge cases (all values missing, all unique values)

3. **Assess Mode Suitability**:
   - Calculate mode frequency percentage
   - Warn if mode frequency is very low (<5%)
   - Consider distribution of categories

4. **Output Requirements**:
   - Return DataFrame with imputed values
   - Include imputation metadata: original_missing_count, imputed_value, mode_frequency, value_counts
   - Generate before/after category distribution plots
   - Report category statistics

5. **Special Considerations**:
   - Handle multiple modes (tie-breaking strategy)
   - Preserve original data types
   - Consider creating "Unknown" category instead of mode for low-frequency modes
   - Report impact on category distribution

## Expected Python Code Structure:
```python
def impute_mode(df, column):
    import pandas as pd
    import numpy as np
    
    # Check for missing values
    missing_count = df[column].isnull().sum()
    if missing_count == 0:
        return df, {'imputed_count': 0, 'method': 'mode'}
    
    # Calculate mode
    mode_result = df[column].mode()
    if len(mode_result) == 0:
        raise ValueError(f"Cannot calculate mode for column {column} - all values are missing")
    
    mode_value = mode_result[0]  # Take first mode if multiple
    
    # Calculate mode statistics
    value_counts = df[column].value_counts()
    mode_frequency = value_counts.iloc[0] if len(value_counts) > 0 else 0
    mode_percentage = (mode_frequency / len(df[column].dropna())) * 100
    
    # Warn if mode frequency is very low
    if mode_percentage < 5:
        print(f"Warning: Mode frequency for {column} is only {mode_percentage:.1f}%")
    
    # Perform imputation
    df_imputed = df.copy()
    df_imputed[column] = df_imputed[column].fillna(mode_value)
    
    # Prepare metadata
    metadata = {
        'column': column,
        'method': 'mode',
        'imputed_count': missing_count,
        'imputed_value': mode_value,
        'mode_frequency': mode_frequency,
        'mode_percentage': mode_percentage,
        'unique_values': df[column].nunique(),
        'total_categories': len(value_counts)
    }
    
    return df_imputed, metadata
```

Generate complete, executable Python code that implements this mode imputation strategy.
"""
)

FillConstant = Strategy(
    id="fill_constant",
    description="Use when a specific placeholder or domain-specific value is needed.",
    prompt="""
You are tasked with imputing missing values using a constant value strategy when domain-specific knowledge suggests a specific replacement value.

## Task Description:
Replace missing values with a predefined constant value based on domain knowledge, business logic, or specific requirements.

## When to Use:
- When missing values have a specific meaning (e.g., 0 for sales in months with no sales)
- Domain-specific default values are known
- When creating explicit "Unknown" or "Not Applicable" categories
- For features where a specific placeholder makes business sense

## Implementation Steps:

1. **Validate Constant Value**:
   ```python
   if constant_value is None:
       raise ValueError("Constant value must be specified")
   ```

2. **Check Data Type Compatibility**:
   - Ensure constant value is compatible with column dtype
   - Handle type conversions if necessary
   - Validate that constant value is appropriate for the feature

3. **Assess Impact**:
   - Calculate percentage of values being replaced
   - Compare with existing value distribution
   - Consider impact on statistical properties

4. **Output Requirements**:
   - Return DataFrame with imputed values
   - Include imputation metadata: original_missing_count, constant_value, impact_percentage
   - Generate before/after distribution comparison
   - Report type compatibility and conversion details

5. **Special Considerations**:
   - Document rationale for chosen constant value
   - Handle edge cases (all values missing, constant already exists)
   - Preserve or convert data types as needed
   - Consider creating new category levels for categorical features

## Expected Python Code Structure:
```python
def fill_constant(df, column, constant_value, rationale=""):
    import pandas as pd
    import numpy as np
    
    # Validate inputs
    if constant_value is None:
        raise ValueError("Constant value must be specified")
    
    # Check for missing values
    missing_count = df[column].isnull().sum()
    if missing_count == 0:
        return df, {'imputed_count': 0, 'method': 'constant'}
    
    # Check data type compatibility
    original_dtype = df[column].dtype
    try:
        # Test if constant value is compatible
        test_series = pd.Series([constant_value], dtype=original_dtype)
        compatible = True
    except (ValueError, TypeError):
        compatible = False
        print(f"Warning: Constant value type may not be compatible with column {column} dtype")
    
    # Calculate impact
    total_count = len(df)
    impact_percentage = (missing_count / total_count) * 100
    
    # Perform imputation
    df_imputed = df.copy()
    df_imputed[column] = df_imputed[column].fillna(constant_value)
    
    # Check if constant value already exists in data
    existing_count = (df[column] == constant_value).sum()
    
    # Prepare metadata
    metadata = {
        'column': column,
        'method': 'constant',
        'imputed_count': missing_count,
        'constant_value': constant_value,
        'impact_percentage': impact_percentage,
        'original_dtype': str(original_dtype),
        'type_compatible': compatible,
        'existing_constant_count': existing_count,
        'rationale': rationale
    }
    
    return df_imputed, metadata
```

Generate complete, executable Python code that implements this constant fill imputation strategy.
"""
)



    
