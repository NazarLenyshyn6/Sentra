"""
This module defines a set of reusable, prompt-driven strategies for handling target analysis
in tabular datasets. Each strategy represents a distinct method of target analysis.
"""

from prompt_engine.src.core.strategy import Strategy

ClassImbalance = Strategy(
    id="class_imbalance",
    description="Use to assess if the target variable has uneven class distributions that may impact model performance.",
    prompt="""
You are tasked with analyzing class imbalance in the target variable to assess its impact on model performance and recommend appropriate strategies.

## Task Description:
Evaluate the distribution of classes in the target variable to identify imbalanced datasets that may require special handling during model training.

## When to Use:
- Classification problems with categorical target variables
- Before model training to assess data quality
- When model performance is unexpectedly poor on minority classes
- For determining if resampling techniques are needed

## Implementation Steps:

1. **Calculate Class Distribution**:
   ```python
   class_counts = df[target_column].value_counts()
   class_proportions = df[target_column].value_counts(normalize=True)
   ```

2. **Assess Imbalance Severity**:
   - Calculate imbalance ratio (majority class / minority class)
   - Identify minority and majority classes
   - Determine severity level (mild, moderate, severe)

3. **Imbalance Metrics**:
   - Imbalance ratio: max_class_count / min_class_count
   - Minority class percentage: min_class_count / total_samples
   - Gini coefficient for multi-class imbalance

4. **Output Requirements**:
   - Return DataFrame with columns: ['class', 'count', 'percentage', 'imbalance_ratio']
   - Include summary statistics: total_classes, imbalance_severity, minority_class_percentage
   - Generate bar plot and pie chart visualizations
   - Provide resampling recommendations

5. **Special Considerations**:
   - Handle multi-class imbalance (>2 classes)
   - Consider business impact of class imbalance
   - Recommend appropriate techniques (SMOTE, undersampling, class weights)
   - Account for stratified sampling requirements

## Expected Python Code Structure:
```python
def analyze_class_imbalance(df, target_column):
    import pandas as pd
    import numpy as np
    
    # Validate target column exists
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in DataFrame")
    
    # Calculate class distribution
    class_counts = df[target_column].value_counts()
    class_proportions = df[target_column].value_counts(normalize=True)
    
    # Calculate imbalance metrics
    max_class_count = class_counts.max()
    min_class_count = class_counts.min()
    imbalance_ratio = max_class_count / min_class_count
    minority_class_percentage = (min_class_count / len(df)) * 100
    
    # Determine imbalance severity
    if imbalance_ratio < 2:
        severity = 'balanced'
    elif imbalance_ratio < 5:
        severity = 'mild_imbalance'
    elif imbalance_ratio < 10:
        severity = 'moderate_imbalance'
    else:
        severity = 'severe_imbalance'
    
    # Create results DataFrame
    results = []
    for class_val in class_counts.index:
        results.append({
            'class': class_val,
            'count': class_counts[class_val],
            'percentage': class_proportions[class_val] * 100,
            'imbalance_ratio': max_class_count / class_counts[class_val]
        })
    
    results_df = pd.DataFrame(results)
    
    # Generate recommendations
    recommendations = []
    if severity == 'severe_imbalance':
        recommendations.extend(['Use SMOTE or ADASYN for oversampling', 'Consider ensemble methods', 'Apply class weights'])
    elif severity == 'moderate_imbalance':
        recommendations.extend(['Consider class weights', 'Use stratified sampling', 'Apply cost-sensitive learning'])
    elif severity == 'mild_imbalance':
        recommendations.extend(['Use stratified sampling', 'Monitor precision/recall metrics'])
    else:
        recommendations.append('No special handling needed')
    
    # Prepare metadata
    metadata = {
        'target_column': target_column,
        'total_classes': len(class_counts),
        'total_samples': len(df),
        'imbalance_ratio': imbalance_ratio,
        'minority_class_percentage': minority_class_percentage,
        'majority_class': class_counts.index[0],
        'minority_class': class_counts.index[-1],
        'imbalance_severity': severity,
        'recommendations': recommendations
    }
    
    return results_df, metadata
```

Generate complete, executable Python code that implements this class imbalance analysis strategy.
"""
)

TargetOutliers = Strategy(
    id="target_outliers",
    description="Use to detect abnormal or extreme target values that could bias model training.",
    prompt="""
You are tasked with detecting outliers in the target variable that could negatively impact model training and prediction quality.

## Task Description:
Identify extreme or abnormal values in the target variable that may represent data errors, rare events, or values that could bias model learning.

## When to Use:
- Regression problems with continuous target variables
- Before model training to ensure data quality
- When model performance is unexpectedly poor
- For detecting data collection or labeling errors

## Implementation Steps:

1. **Validate Target Type**:
   ```python
   if not pd.api.types.is_numeric_dtype(df[target_column]):
       raise ValueError("Target outlier detection requires numeric target")
   ```

2. **Apply Multiple Detection Methods**:
   - IQR method for robust detection
   - Z-Score method for normal distributions
   - Modified Z-Score for skewed distributions
   - Isolation Forest for complex outliers

3. **Assess Outlier Impact**:
   - Calculate outlier severity and frequency
   - Analyze distribution before/after outlier removal
   - Estimate impact on model performance

4. **Output Requirements**:
   - Return DataFrame with columns: ['index', 'target_value', 'outlier_method', 'outlier_score', 'severity']
   - Include summary statistics: outlier_count, outlier_percentage, impact_on_mean/std
   - Generate distribution plots with outliers highlighted
   - Provide recommendations for handling outliers

5. **Special Considerations**:
   - Consider domain knowledge (are outliers valid?)
   - Assess business impact of removing outliers
   - Handle different outlier types (univariate vs multivariate)
   - Recommend appropriate treatment strategies

## Expected Python Code Structure:
```python
def detect_target_outliers(df, target_column):
    import pandas as pd
    import numpy as np
    from sklearn.ensemble import IsolationForest
    
    # Validate target column
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in DataFrame")
    
    if not pd.api.types.is_numeric_dtype(df[target_column]):
        raise ValueError("Target outlier detection requires numeric target")
    
    # Remove missing values
    target_data = df[target_column].dropna()
    if len(target_data) == 0:
        return pd.DataFrame(), {'outlier_count': 0}
    
    outliers_results = []
    
    # Method 1: IQR
    Q1 = target_data.quantile(0.25)
    Q3 = target_data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    iqr_outliers = target_data[(target_data < lower_bound) | (target_data > upper_bound)]
    
    # Method 2: Z-Score
    mean_val = target_data.mean()
    std_val = target_data.std()
    z_scores = np.abs((target_data - mean_val) / std_val)
    zscore_outliers = target_data[z_scores > 3]
    
    # Method 3: Modified Z-Score
    median_val = target_data.median()
    mad_val = target_data.mad()
    if mad_val > 0:
        modified_z_scores = 0.6745 * np.abs(target_data - median_val) / mad_val
        mod_zscore_outliers = target_data[modified_z_scores > 3.5]
    else:
        mod_zscore_outliers = pd.Series([], dtype=target_data.dtype)
    
    # Method 4: Isolation Forest
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    outlier_labels = iso_forest.fit_predict(target_data.values.reshape(-1, 1))
    isolation_outliers = target_data[outlier_labels == -1]
    
    # Combine results
    all_outliers = pd.concat([iqr_outliers, zscore_outliers, mod_zscore_outliers, isolation_outliers]).drop_duplicates()
    
    # Create detailed results
    for idx, value in all_outliers.items():
        methods = []
        scores = []
        
        if idx in iqr_outliers.index:
            methods.append('IQR')
            if value < lower_bound:
                scores.append(abs(value - lower_bound))
            else:
                scores.append(abs(value - upper_bound))
        
        if idx in zscore_outliers.index:
            methods.append('Z-Score')
            scores.append(abs(z_scores[idx]))
        
        if idx in mod_zscore_outliers.index:
            methods.append('Modified Z-Score')
            scores.append(abs(modified_z_scores[idx]))
        
        if idx in isolation_outliers.index:
            methods.append('Isolation Forest')
            scores.append(1.0)  # Binary for isolation forest
        
        severity = 'extreme' if len(methods) >= 3 else 'moderate' if len(methods) == 2 else 'mild'
        
        outliers_results.append({
            'index': idx,
            'target_value': value,
            'outlier_methods': ', '.join(methods),
            'max_outlier_score': max(scores) if scores else 0,
            'severity': severity,
            'method_count': len(methods)
        })
    
    outliers_df = pd.DataFrame(outliers_results)
    
    # Calculate impact statistics
    original_mean = target_data.mean()
    original_std = target_data.std()
    
    if len(outliers_df) > 0:
        cleaned_data = target_data.drop(outliers_df['index'])
        cleaned_mean = cleaned_data.mean()
        cleaned_std = cleaned_data.std()
        mean_impact = abs(original_mean - cleaned_mean)
        std_impact = abs(original_std - cleaned_std)
    else:
        mean_impact = 0
        std_impact = 0
    
    # Generate recommendations
    recommendations = []
    outlier_percentage = (len(outliers_df) / len(target_data)) * 100
    
    if outlier_percentage > 10:
        recommendations.append('High outlier rate - investigate data collection process')
    if outlier_percentage > 5:
        recommendations.append('Consider robust regression methods')
    if outlier_percentage > 1:
        recommendations.append('Apply outlier treatment (capping, transformation)')
    else:
        recommendations.append('Outlier rate is acceptable')
    
    # Prepare metadata
    metadata = {
        'target_column': target_column,
        'total_samples': len(target_data),
        'outlier_count': len(outliers_df),
        'outlier_percentage': outlier_percentage,
        'original_mean': original_mean,
        'original_std': original_std,
        'mean_impact': mean_impact,
        'std_impact': std_impact,
        'extreme_outliers': len(outliers_df[outliers_df['severity'] == 'extreme']),
        'moderate_outliers': len(outliers_df[outliers_df['severity'] == 'moderate']),
        'mild_outliers': len(outliers_df[outliers_df['severity'] == 'mild']),
        'recommendations': recommendations
    }
    
    return outliers_df, metadata
```

Generate complete, executable Python code that implements this target outlier detection strategy.
"""
)



