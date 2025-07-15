"""
This module defines a set of reusable, prompt-driven strategies for handling outliers detection
in tabular datasets. Each strategy represents a distinct method of outliers detection.
"""

from prompt_engine.src.core.strategy import Strategy

ZScore = Strategy(
    id="z_score",
    description="Use to detect outliers in normally distributed data by measuring how many standard deviations a point is from the mean.",
    prompt="""
You are tasked with detecting outliers using the Z-Score method for normally distributed numeric data.

## Task Description:
Identify outliers by calculating how many standard deviations each data point is from the mean, suitable for normally distributed data.

## When to Use:
- Numeric features with approximately normal distribution
- When data has low skewness (typically |skewness| < 0.5)
- For detecting extreme values based on standard deviations
- When the mean and standard deviation are meaningful measures

## Implementation Steps:

1. **Validate Distribution**:
   ```python
   skewness = df[column].skew()
   if abs(skewness) > 1:
       print(f"Warning: Data is highly skewed (skewness={skewness:.2f})")
   ```

2. **Calculate Z-Scores**:
   - Compute mean and standard deviation
   - Calculate Z-score for each data point: (value - mean) / std
   - Apply threshold (typically |z| > 3 for outliers)

3. **Identify Outliers**:
   - Flag values with |z-score| > threshold
   - Separate mild outliers (2 < |z| < 3) and extreme outliers (|z| > 3)

4. **Output Requirements**:
   - Return DataFrame with columns: ['index', 'value', 'z_score', 'is_outlier', 'outlier_type']
   - Include summary statistics: outlier_count, outlier_percentage, mean, std
   - Generate visualization (histogram with outliers highlighted)
   - Report distribution statistics

5. **Special Considerations**:
   - Handle missing values before calculation
   - Consider impact of outliers on mean and std calculation
   - Provide different thresholds for mild vs extreme outliers
   - Consider using robust statistics if distribution is questionable

## Expected Python Code Structure:
```python
def detect_outliers_zscore(df, column, threshold=3):
    import pandas as pd
    import numpy as np
    from scipy import stats
    
    # Validate numeric column
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column {column} must be numeric")
    
    # Remove missing values
    data = df[column].dropna()
    if len(data) == 0:
        return pd.DataFrame(), {'outlier_count': 0}
    
    # Check distribution
    skewness = data.skew()
    if abs(skewness) > 1:
        print(f"Warning: Data is highly skewed (skewness={skewness:.2f}), consider using Modified Z-Score")
    
    # Calculate Z-scores
    mean_val = data.mean()
    std_val = data.std()
    z_scores = np.abs((data - mean_val) / std_val)
    
    # Identify outliers
    outliers_mask = z_scores > threshold
    mild_outliers_mask = (z_scores > 2) & (z_scores <= 3)
    extreme_outliers_mask = z_scores > 3
    
    # Create results DataFrame
    results = pd.DataFrame({
        'index': data.index,
        'value': data.values,
        'z_score': z_scores,
        'is_outlier': outliers_mask,
        'outlier_type': np.where(extreme_outliers_mask, 'extreme', 
                                np.where(mild_outliers_mask, 'mild', 'normal'))
    })
    
    # Filter to outliers only
    outliers_df = results[results['is_outlier']].copy()
    
    # Prepare metadata
    metadata = {
        'column': column,
        'method': 'z_score',
        'threshold': threshold,
        'outlier_count': len(outliers_df),
        'outlier_percentage': (len(outliers_df) / len(data)) * 100,
        'mean': mean_val,
        'std': std_val,
        'skewness': skewness,
        'extreme_outliers': (extreme_outliers_mask).sum(),
        'mild_outliers': (mild_outliers_mask).sum()
    }
    
    return outliers_df, metadata
```

Generate complete, executable Python code that implements this Z-Score outlier detection strategy.
"""
)

ModifiedZScore = Strategy(
    id="modified_z_score",
    description="Use to detect outliers in data with potential skew or non-normality, using median and MAD.",
    prompt="""
You are tasked with detecting outliers using the Modified Z-Score method for skewed or non-normal numeric data using median and MAD.

## Task Description:
Identify outliers using median and Median Absolute Deviation (MAD) instead of mean and standard deviation, more robust to skewed data.

## When to Use:
- Numeric features with skewed distributions
- When data contains existing outliers that affect mean/std
- For robust outlier detection less sensitive to extreme values
- When median is more representative than mean

## Implementation Steps:

1. **Calculate Robust Statistics**:
   ```python
   median = df[column].median()
   mad = df[column].mad()  # Median Absolute Deviation
   ```

2. **Calculate Modified Z-Scores**:
   - Modified Z-Score = 0.6745 * (value - median) / MAD
   - The constant 0.6745 makes MAD comparable to standard deviation
   - Apply threshold (typically |modified_z| > 3.5 for outliers)

3. **Identify Outliers**:
   - Flag values with |modified_z_score| > threshold
   - Less sensitive to extreme values than standard Z-Score
   - Better performance on skewed distributions

4. **Output Requirements**:
   - Return DataFrame with columns: ['index', 'value', 'modified_z_score', 'is_outlier', 'outlier_type']
   - Include summary statistics: outlier_count, outlier_percentage, median, mad
   - Generate visualization comparing with standard Z-Score
   - Report robustness metrics

5. **Special Considerations**:
   - Handle zero MAD (constant data) by using small epsilon
   - Compare results with standard Z-Score method
   - More conservative than standard Z-Score (fewer false positives)
   - Better suited for financial, biological, or skewed data

## Expected Python Code Structure:
```python
def detect_outliers_modified_zscore(df, column, threshold=3.5):
    import pandas as pd
    import numpy as np
    
    # Validate numeric column
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column {column} must be numeric")
    
    # Remove missing values
    data = df[column].dropna()
    if len(data) == 0:
        return pd.DataFrame(), {'outlier_count': 0}
    
    # Calculate robust statistics
    median_val = data.median()
    mad_val = data.mad()
    
    # Handle zero MAD (constant data)
    if mad_val == 0:
        mad_val = np.finfo(float).eps  # Small epsilon
        print("Warning: MAD is zero, using small epsilon")
    
    # Calculate modified Z-scores
    modified_z_scores = 0.6745 * (data - median_val) / mad_val
    abs_modified_z_scores = np.abs(modified_z_scores)
    
    # Identify outliers
    outliers_mask = abs_modified_z_scores > threshold
    mild_outliers_mask = (abs_modified_z_scores > 2.5) & (abs_modified_z_scores <= 3.5)
    extreme_outliers_mask = abs_modified_z_scores > 3.5
    
    # Create results DataFrame
    results = pd.DataFrame({
        'index': data.index,
        'value': data.values,
        'modified_z_score': modified_z_scores,
        'abs_modified_z_score': abs_modified_z_scores,
        'is_outlier': outliers_mask,
        'outlier_type': np.where(extreme_outliers_mask, 'extreme', 
                                np.where(mild_outliers_mask, 'mild', 'normal'))
    })
    
    # Filter to outliers only
    outliers_df = results[results['is_outlier']].copy()
    
    # Compare with standard Z-Score
    mean_val = data.mean()
    std_val = data.std()
    z_scores = np.abs((data - mean_val) / std_val)
    standard_outliers = (z_scores > 3).sum()
    
    # Prepare metadata
    metadata = {
        'column': column,
        'method': 'modified_z_score',
        'threshold': threshold,
        'outlier_count': len(outliers_df),
        'outlier_percentage': (len(outliers_df) / len(data)) * 100,
        'median': median_val,
        'mad': mad_val,
        'skewness': data.skew(),
        'extreme_outliers': (extreme_outliers_mask).sum(),
        'mild_outliers': (mild_outliers_mask).sum(),
        'standard_z_outliers': standard_outliers,
        'robustness_ratio': len(outliers_df) / max(standard_outliers, 1)
    }
    
    return outliers_df, metadata
```

Generate complete, executable Python code that implements this Modified Z-Score outlier detection strategy.
"""
)

IQR = Strategy(
    id="iqr",
    description="Use to detect outliers based on the interquartile range, effective for skewed distributions.",
    prompt="""
You are tasked with detecting outliers using the Interquartile Range (IQR) method, effective for skewed distributions and non-parametric data.

## Task Description:
Identify outliers using the IQR method by flagging values that fall outside the range [Q1 - 1.5*IQR, Q3 + 1.5*IQR], where IQR = Q3 - Q1.

## When to Use:
- Any distribution type (robust, non-parametric method)
- Skewed distributions where Z-Score methods fail
- When you want a simple, interpretable outlier detection method
- For exploratory data analysis and data visualization

## Implementation Steps:

1. **Calculate Quartiles**:
   ```python
   Q1 = df[column].quantile(0.25)
   Q3 = df[column].quantile(0.75)
   IQR = Q3 - Q1
   ```

2. **Define Outlier Bounds**:
   - Lower bound = Q1 - 1.5 * IQR
   - Upper bound = Q3 + 1.5 * IQR
   - Extreme outliers: Q1 - 3 * IQR or Q3 + 3 * IQR

3. **Identify Outliers**:
   - Flag values outside [lower_bound, upper_bound]
   - Categorize as mild (1.5*IQR) or extreme (3*IQR) outliers
   - Separate upper and lower outliers

4. **Output Requirements**:
   - Return DataFrame with columns: ['index', 'value', 'outlier_type', 'bound_exceeded', 'distance_from_bound']
   - Include summary statistics: outlier_count, outlier_percentage, Q1, Q3, IQR
   - Generate box plot visualization
   - Report outlier boundaries and statistics

5. **Special Considerations**:
   - Handle zero IQR (constant data) gracefully
   - Consider different multipliers (1.5 for mild, 3 for extreme)
   - Works well with box plots and quartile-based analysis
   - Less sensitive to distribution shape than Z-Score methods

## Expected Python Code Structure:
```python
def detect_outliers_iqr(df, column, multiplier=1.5):
    import pandas as pd
    import numpy as np
    
    # Validate numeric column
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column {column} must be numeric")
    
    # Remove missing values
    data = df[column].dropna()
    if len(data) == 0:
        return pd.DataFrame(), {'outlier_count': 0}
    
    # Calculate quartiles and IQR
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    
    # Handle zero IQR (constant data)
    if IQR == 0:
        return pd.DataFrame(), {'outlier_count': 0, 'warning': 'Zero IQR - no outliers detected'}
    
    # Calculate bounds
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    extreme_lower = Q1 - 3 * IQR
    extreme_upper = Q3 + 3 * IQR
    
    # Identify outliers
    outliers_mask = (data < lower_bound) | (data > upper_bound)
    extreme_outliers_mask = (data < extreme_lower) | (data > extreme_upper)
    
    # Create results DataFrame
    results = []
    for idx, value in data.items():
        if outliers_mask[idx]:
            if extreme_outliers_mask[idx]:
                outlier_type = 'extreme'
            else:
                outlier_type = 'mild'
            
            if value < lower_bound:
                bound_exceeded = 'lower'
                distance = lower_bound - value
            else:
                bound_exceeded = 'upper'
                distance = value - upper_bound
            
            results.append({
                'index': idx,
                'value': value,
                'outlier_type': outlier_type,
                'bound_exceeded': bound_exceeded,
                'distance_from_bound': distance
            })
    
    outliers_df = pd.DataFrame(results)
    
    # Count outliers by type
    mild_outliers = (outliers_mask & ~extreme_outliers_mask).sum()
    extreme_outliers_count = extreme_outliers_mask.sum()
    
    # Prepare metadata
    metadata = {
        'column': column,
        'method': 'iqr',
        'multiplier': multiplier,
        'outlier_count': len(outliers_df),
        'outlier_percentage': (len(outliers_df) / len(data)) * 100,
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'mild_outliers': mild_outliers,
        'extreme_outliers': extreme_outliers_count,
        'upper_outliers': ((data > upper_bound) & outliers_mask).sum(),
        'lower_outliers': ((data < lower_bound) & outliers_mask).sum()
    }
    
    return outliers_df, metadata
```

Generate complete, executable Python code that implements this IQR outlier detection strategy.
"""
)

