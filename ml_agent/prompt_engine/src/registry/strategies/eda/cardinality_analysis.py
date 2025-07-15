"""
This module defines a set of reusable, prompt-driven strategies for handling cardinality analysis.
Each strategy represents a distinct method of cardinality analysis.
"""

from prompt_engine.src.core.strategy import Strategy


UniqueRatio = Strategy(
    id="unique_ratio",
    description="Use to identify features with a high or low ratio of unique values, "
                "indicating whether a feature is categorical or continuous.",
    prompt="""
You are tasked with analyzing the cardinality of features in a dataset to determine whether they are categorical or continuous based on their unique value ratios.

## Task Description:
Calculate the ratio of unique values to total values for each feature to classify features as categorical or continuous.

## When to Use:
- Initial feature assessment during EDA
- Feature type classification before modeling
- Identifying features that need different preprocessing approaches
- Detecting features with too many categories for standard categorical encoding

## Implementation Steps:

1. **Calculate Unique Ratio**:
   ```python
   unique_ratio = df[column].nunique() / len(df)
   ```

2. **Classification Thresholds**:
   - High cardinality (continuous-like): ratio > 0.5
   - Medium cardinality: 0.05 < ratio <= 0.5
   - Low cardinality (categorical): ratio <= 0.05

3. **Analysis Methods**:
   - Use `df.nunique()` to get unique counts
   - Calculate ratios for all columns at once
   - Create summary statistics and visualizations

4. **Output Requirements**:
   - Return a DataFrame with columns: ['feature', 'unique_count', 'total_count', 'unique_ratio', 'suggested_type']
   - Include summary statistics (mean, median, std of ratios)
   - Generate bar plot showing unique ratios by feature

5. **Special Considerations**:
   - Handle missing values appropriately
   - Consider string columns that might be numeric
   - Flag features with extremely high cardinality (>95% unique)
   - Identify potential ID columns (100% unique)

## Expected Python Code Structure:
```python
def analyze_cardinality(df):
    results = []
    for col in df.columns:
        unique_count = df[col].nunique()
        total_count = len(df)
        unique_ratio = unique_count / total_count
        
        if unique_ratio > 0.5:
            suggested_type = 'continuous'
        elif unique_ratio > 0.05:
            suggested_type = 'categorical_medium'
        else:
            suggested_type = 'categorical_low'
            
        results.append({
            'feature': col,
            'unique_count': unique_count,
            'total_count': total_count,
            'unique_ratio': unique_ratio,
            'suggested_type': suggested_type
        })
    
    return pd.DataFrame(results)
```

Generate complete, executable Python code that implements this cardinality analysis strategy.
"""
)

TagLowCardinality = Strategy(
    id="tag_low_cardinality",
    description="Use to flag features with very few unique values for specialized encoding or aggregation.",
    prompt="""
You are tasked with identifying and flagging features that have very few unique values (low cardinality) for specialized preprocessing treatment.

## Task Description:
Identify features with extremely low cardinality that may require special handling such as binary encoding, one-hot encoding, or feature aggregation.

## When to Use:
- Before applying categorical encoding techniques
- When identifying features that might be binary or near-binary
- For feature engineering decisions (drop, encode, or aggregate)
- When optimizing memory usage and model performance

## Implementation Steps:

1. **Define Low Cardinality Threshold**:
   ```python
   threshold = 10  # or dynamic: max(2, int(len(df) * 0.01))
   ```

2. **Identify Low Cardinality Features**:
   - Count unique values per feature
   - Flag features with unique count <= threshold
   - Separate numeric and categorical low cardinality features

3. **Analysis Methods**:
   - Calculate value counts for each low cardinality feature
   - Determine if feature is binary (2 unique values)
   - Check for features with single unique value (constants)

4. **Output Requirements**:
   - Return DataFrame with columns: ['feature', 'unique_count', 'unique_values', 'is_binary', 'is_constant', 'dtype', 'encoding_suggestion']
   - Include value counts for each flagged feature
   - Provide encoding recommendations

5. **Special Considerations**:
   - Handle missing values in unique count calculations
   - Consider string representation of numeric categories
   - Flag potential constant features (single unique value)
   - Distinguish between truly categorical and ordinal features

## Expected Python Code Structure:
```python
def tag_low_cardinality(df, threshold=10):
    low_cardinality_features = []
    
    for col in df.columns:
        unique_count = df[col].nunique()
        
        if unique_count <= threshold:
            unique_values = df[col].unique()
            is_binary = unique_count == 2
            is_constant = unique_count == 1
            
            if is_constant:
                encoding_suggestion = 'drop'
            elif is_binary:
                encoding_suggestion = 'binary_encode'
            else:
                encoding_suggestion = 'one_hot_encode'
            
            low_cardinality_features.append({
                'feature': col,
                'unique_count': unique_count,
                'unique_values': unique_values,
                'is_binary': is_binary,
                'is_constant': is_constant,
                'dtype': str(df[col].dtype),
                'encoding_suggestion': encoding_suggestion
            })
    
    return pd.DataFrame(low_cardinality_features)
```

Generate complete, executable Python code that implements this low cardinality tagging strategy.
"""
)

