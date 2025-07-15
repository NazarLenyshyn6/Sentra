"""
This module defines a set of reusable, prompt-driven strategies for handling data ingestion.
Each strategy represents a distinct method of data ingestion.
"""

from prompt_engine.src.core.strategy import Strategy


CSV = Strategy(
    id="csv",
    description="Use for ingesting datasets in CSV format, commonly used for tabular data.",
    prompt="""
You are tasked with ingesting CSV datasets efficiently and robustly, handling various CSV formats and potential data quality issues.

## Task Description:
Load CSV files into pandas DataFrames with proper data type inference, encoding detection, and error handling.

## When to Use:
- Loading tabular datasets stored in CSV format
- Initial data ingestion step in EDA pipeline
- When dealing with comma-separated or other delimiter-separated files
- Processing CSV files with various encodings and formats

## Implementation Steps:

1. **File Validation**:
   ```python
   import os
   if not os.path.exists(file_path):
       raise FileNotFoundError(f"CSV file not found: {file_path}")
   ```

2. **Encoding Detection**:
   - Use chardet library to detect file encoding
   - Try common encodings: utf-8, latin-1, cp1252
   - Handle encoding errors gracefully

3. **CSV Loading Parameters**:
   - Auto-detect delimiter (comma, semicolon, tab)
   - Handle various quote characters
   - Skip blank lines and comments
   - Infer data types automatically

4. **Output Requirements**:
   - Return pandas DataFrame with properly typed columns
   - Include metadata: file_path, shape, dtypes, encoding_used
   - Report any loading warnings or issues
   - Display basic dataset information

5. **Special Considerations**:
   - Handle large files with chunking if needed
   - Detect and handle malformed CSV rows
   - Preserve original column names
   - Handle missing values appropriately during loading

## Expected Python Code Structure:
```python
def load_csv(file_path, **kwargs):
    import pandas as pd
    import chardet
    import os
    
    # Validate file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    
    # Detect encoding
    with open(file_path, 'rb') as f:
        encoding = chardet.detect(f.read())['encoding']
    
    # Try loading with detected encoding
    try:
        df = pd.read_csv(
            file_path,
            encoding=encoding,
            low_memory=False,
            **kwargs
        )
    except UnicodeDecodeError:
        # Fallback to utf-8 with error handling
        df = pd.read_csv(
            file_path,
            encoding='utf-8',
            errors='replace',
            low_memory=False,
            **kwargs
        )
    
    # Return DataFrame with metadata
    metadata = {
        'file_path': file_path,
        'shape': df.shape,
        'dtypes': df.dtypes.to_dict(),
        'encoding_used': encoding
    }
    
    return df, metadata
```

Generate complete, executable Python code that implements this CSV ingestion strategy.
"""
)

