import pandas as pd
import numpy as np

def load_data(file):
    """Load data from uploaded file"""
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format")

def get_numeric_columns(df):
    """Return list of numeric columns"""
    return df.select_dtypes(include=[np.number]).columns.tolist()

def get_categorical_columns(df):
    """Return list of categorical columns"""
    return df.select_dtypes(include=['object', 'category']).columns.tolist()

def calculate_summary_stats(df):
    """Calculate basic summary statistics"""
    numeric_stats = df.describe()
    categorical_stats = df.describe(include=['object', 'category'])
    missing_values = df.isnull().sum()
    return numeric_stats, categorical_stats, missing_values
