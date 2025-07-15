"""
This module defines a set of reusable, prompt-driven strategies for handling type_handling
in tabular datasets. Each strategy represents a distinct method of type_handling.
"""

from prompt_engine.src.core.strategy import Strategy


ParseDatetime = Strategy(
    id="parse_datetime",
    description="Use to convert columns containing date or time information into datetime objects for easier analysis.",
    prompt="""
You are tasked with parsing and converting columns containing date or time information into proper datetime objects for temporal analysis.

## Task Description:
Identify and convert string or numeric columns containing date/time information into pandas datetime objects, enabling time-based analysis and operations.

## When to Use:
- Columns containing date/time strings in various formats
- Numeric columns representing timestamps or date components
- Before performing time series analysis
- When extracting temporal features for modeling

## Implementation Steps:

1. **Detect Date/Time Columns**:
   ```python
   # Sample data to detect patterns
   sample_data = df[column].dropna().head(100)
   ```

2. **Identify Date/Time Formats**:
   - Common formats: 'YYYY-MM-DD', 'MM/DD/YYYY', 'DD-MM-YYYY'
   - Timestamp formats: Unix timestamps, ISO format
   - Mixed formats requiring flexible parsing

3. **Parse with Error Handling**:
   - Use pd.to_datetime() with infer_datetime_format=True
   - Handle multiple formats in same column
   - Manage parsing errors gracefully

4. **Output Requirements**:
   - Return DataFrame with converted datetime columns
   - Include conversion metadata: original_format, conversion_success_rate, invalid_dates
   - Generate temporal analysis summary (date range, frequency)
   - Report parsing issues and recommendations

5. **Special Considerations**:
   - Handle timezone information
   - Manage ambiguous date formats (MM/DD vs DD/MM)
   - Extract additional temporal features (year, month, day, hour)
   - Consider localization and regional date formats

## Expected Python Code Structure:
```python
def parse_datetime(df, column, format_hint=None):
    import pandas as pd
    import numpy as np
    from datetime import datetime
    
    # Validate column exists
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    # Get non-null values
    original_data = df[column].dropna()
    if len(original_data) == 0:
        return df, {'conversion_count': 0, 'success_rate': 0}
    
    # Try different conversion strategies
    conversion_attempts = []
    
    # Strategy 1: Direct conversion with format hint
    if format_hint:
        try:
            converted = pd.to_datetime(df[column], format=format_hint, errors='coerce')
            success_rate = (converted.notna().sum() / len(original_data)) * 100
            conversion_attempts.append(('format_hint', converted, success_rate))
        except Exception as e:
            print(f"Format hint failed: {e}")
    
    # Strategy 2: Automatic inference
    try:
        converted = pd.to_datetime(df[column], infer_datetime_format=True, errors='coerce')
        success_rate = (converted.notna().sum() / len(original_data)) * 100
        conversion_attempts.append(('auto_infer', converted, success_rate))
    except Exception as e:
        print(f"Auto inference failed: {e}")
    
    # Strategy 3: Unix timestamp conversion
    if df[column].dtype in ['int64', 'float64']:
        try:
            # Try seconds timestamp
            converted = pd.to_datetime(df[column], unit='s', errors='coerce')
            success_rate = (converted.notna().sum() / len(original_data)) * 100
            conversion_attempts.append(('unix_seconds', converted, success_rate))
            
            # Try milliseconds timestamp
            converted = pd.to_datetime(df[column], unit='ms', errors='coerce')
            success_rate = (converted.notna().sum() / len(original_data)) * 100
            conversion_attempts.append(('unix_milliseconds', converted, success_rate))
        except Exception as e:
            print(f"Unix timestamp conversion failed: {e}")
    
    # Strategy 4: Multiple format attempts
    common_formats = [
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%Y-%m-%d %H:%M:%S',
        '%m/%d/%Y %H:%M:%S',
        '%Y%m%d'
    ]
    
    for fmt in common_formats:
        try:
            converted = pd.to_datetime(df[column], format=fmt, errors='coerce')
            success_rate = (converted.notna().sum() / len(original_data)) * 100
            if success_rate > 0:
                conversion_attempts.append((f'format_{fmt}', converted, success_rate))
        except:
            continue
    
    # Select best conversion
    if conversion_attempts:
        best_conversion = max(conversion_attempts, key=lambda x: x[2])
        method, converted_series, success_rate = best_conversion
        
        # Apply conversion
        df_converted = df.copy()
        df_converted[column] = converted_series
        
        # Extract temporal features
        if success_rate > 50:  # Only if conversion was reasonably successful
            df_converted[f'{column}_year'] = converted_series.dt.year
            df_converted[f'{column}_month'] = converted_series.dt.month
            df_converted[f'{column}_day'] = converted_series.dt.day
            df_converted[f'{column}_dayofweek'] = converted_series.dt.dayofweek
            df_converted[f'{column}_hour'] = converted_series.dt.hour
            
            # Calculate date range
            valid_dates = converted_series.dropna()
            if len(valid_dates) > 0:
                date_range = (valid_dates.max() - valid_dates.min()).days
                min_date = valid_dates.min()
                max_date = valid_dates.max()
            else:
                date_range = 0
                min_date = None
                max_date = None
        else:
            date_range = 0
            min_date = None
            max_date = None
        
        # Count invalid dates
        invalid_count = len(original_data) - converted_series.notna().sum()
        
        # Prepare metadata
        metadata = {
            'column': column,
            'conversion_method': method,
            'total_values': len(original_data),
            'converted_values': converted_series.notna().sum(),
            'invalid_values': invalid_count,
            'success_rate': success_rate,
            'date_range_days': date_range,
            'min_date': min_date,
            'max_date': max_date,
            'temporal_features_created': success_rate > 50
        }
        
        return df_converted, metadata
    
    else:
        # No conversion successful
        return df, {
            'column': column,
            'conversion_method': 'none',
            'success_rate': 0,
            'error': 'No successful datetime conversion found'
        }
```

Generate complete, executable Python code that implements this datetime parsing strategy.
"""
)

ConvertObjectToNumeric = Strategy(
    id="convert_object_to_numeric",
    description="Use to convert object-type columns containing numeric values into proper numeric dtype.",
    prompt="""
You are tasked with converting object-type columns that contain numeric values into proper numeric data types for analysis and modeling.

## Task Description:
Identify and convert string/object columns containing numeric data into appropriate numeric dtypes (int, float), handling various formatting issues and conversion errors.

## When to Use:
- Object columns containing numeric values stored as strings
- Columns with numbers mixed with formatting (commas, currency symbols, percentages)
- After data import where numeric columns were interpreted as objects
- Before performing mathematical operations or statistical analysis

## Implementation Steps:

1. **Identify Numeric-Like Columns**:
   ```python
   # Sample data to identify numeric patterns
   sample_data = df[column].dropna().head(100)
   ```

2. **Clean and Preprocess**:
   - Remove currency symbols ($, €, £)
   - Remove thousand separators (commas, spaces)
   - Handle percentage symbols (%)
   - Strip whitespace and special characters

3. **Attempt Conversion**:
   - Try pd.to_numeric() with different error handling
   - Handle mixed data types gracefully
   - Preserve original data for fallback

4. **Output Requirements**:
   - Return DataFrame with converted numeric columns
   - Include conversion metadata: conversion_success_rate, invalid_values, detected_format
   - Generate before/after comparison statistics
   - Report conversion issues and data quality problems

5. **Special Considerations**:
   - Handle scientific notation (1e5, 1.5e-3)
   - Manage locale-specific number formats
   - Preserve precision for financial data
   - Handle mixed integer/float detection

## Expected Python Code Structure:
```python
def convert_object_to_numeric(df, column):
    import pandas as pd
    import numpy as np
    import re
    
    # Validate column exists and is object type
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    if df[column].dtype != 'object':
        return df, {'conversion_needed': False, 'original_dtype': str(df[column].dtype)}
    
    # Get non-null values
    original_data = df[column].dropna()
    if len(original_data) == 0:
        return df, {'conversion_count': 0, 'success_rate': 0}
    
    # Create working copy
    working_series = original_data.copy()
    
    # Step 1: Identify numeric patterns
    numeric_pattern = r'^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$'
    currency_pattern = r'[\$€£¥₹]'
    percentage_pattern = r'%'
    comma_pattern = r','
    
    # Step 2: Clean the data
    cleaned_series = working_series.astype(str)
    
    # Remove currency symbols
    cleaned_series = cleaned_series.str.replace(currency_pattern, '', regex=True)
    
    # Handle percentages (convert to decimal)
    percentage_mask = cleaned_series.str.contains(percentage_pattern, na=False)
    cleaned_series = cleaned_series.str.replace(percentage_pattern, '', regex=True)
    
    # Remove thousand separators
    cleaned_series = cleaned_series.str.replace(comma_pattern, '', regex=True)
    
    # Strip whitespace
    cleaned_series = cleaned_series.str.strip()
    
    # Remove any remaining non-numeric characters except decimal point, minus sign, and scientific notation
    cleaned_series = cleaned_series.str.replace(r'[^\d\.\-\+eE]', '', regex=True)
    
    # Step 3: Attempt conversion
    conversion_attempts = []
    
    # Attempt 1: Direct conversion
    try:
        converted = pd.to_numeric(cleaned_series, errors='coerce')
        
        # Apply percentage conversion if needed
        if percentage_mask.any():
            converted.loc[percentage_mask] = converted.loc[percentage_mask] / 100
        
        success_rate = (converted.notna().sum() / len(original_data)) * 100
        conversion_attempts.append(('direct', converted, success_rate))
    except Exception as e:
        print(f"Direct conversion failed: {e}")
    
    # Attempt 2: Try with different decimal separators
    try:
        # Handle European format (comma as decimal separator)
        euro_format = cleaned_series.str.replace(r'\.', '_temp_', regex=True)
        euro_format = euro_format.str.replace(r',', '.', regex=True)
        euro_format = euro_format.str.replace(r'_temp_', '', regex=True)
        
        converted = pd.to_numeric(euro_format, errors='coerce')
        success_rate = (converted.notna().sum() / len(original_data)) * 100
        conversion_attempts.append(('euro_format', converted, success_rate))
    except Exception as e:
        print(f"Euro format conversion failed: {e}")
    
    # Select best conversion
    if conversion_attempts:
        best_conversion = max(conversion_attempts, key=lambda x: x[2])
        method, converted_series, success_rate = best_conversion
        
        # Determine optimal numeric type
        if success_rate > 0:
            # Check if all values are integers
            non_null_converted = converted_series.dropna()
            if len(non_null_converted) > 0 and (non_null_converted % 1 == 0).all():
                # Check if values fit in int64
                if (non_null_converted >= np.iinfo(np.int64).min).all() and (non_null_converted <= np.iinfo(np.int64).max).all():
                    final_dtype = 'int64'
                    converted_series = converted_series.astype('Int64')  # Nullable integer
                else:
                    final_dtype = 'float64'
            else:
                final_dtype = 'float64'
        else:
            final_dtype = 'object'  # Keep as object if conversion failed
        
        # Apply conversion to DataFrame
        df_converted = df.copy()
        if success_rate > 50:  # Only convert if reasonably successful
            df_converted[column] = converted_series
        
        # Calculate statistics
        invalid_count = len(original_data) - converted_series.notna().sum()
        
        # Detect common formats
        detected_formats = []
        if percentage_mask.any():
            detected_formats.append('percentage')
        if original_data.str.contains(currency_pattern, na=False).any():
            detected_formats.append('currency')
        if original_data.str.contains(comma_pattern, na=False).any():
            detected_formats.append('thousands_separator')
        
        # Calculate conversion impact
        if success_rate > 0:
            converted_mean = converted_series.mean()
            converted_std = converted_series.std()
            min_val = converted_series.min()
            max_val = converted_series.max()
        else:
            converted_mean = converted_std = min_val = max_val = None
        
        # Prepare metadata
        metadata = {
            'column': column,
            'conversion_method': method,
            'original_dtype': 'object',
            'final_dtype': final_dtype,
            'total_values': len(original_data),
            'converted_values': converted_series.notna().sum(),
            'invalid_values': invalid_count,
            'success_rate': success_rate,
            'detected_formats': detected_formats,
            'mean': converted_mean,
            'std': converted_std,
            'min': min_val,
            'max': max_val,
            'conversion_applied': success_rate > 50
        }
        
        return df_converted, metadata
    
    else:
        # No conversion successful
        return df, {
            'column': column,
            'conversion_method': 'none',
            'success_rate': 0,
            'error': 'No successful numeric conversion found'
        }
```

Generate complete, executable Python code that implements this object-to-numeric conversion strategy.
"""
)



