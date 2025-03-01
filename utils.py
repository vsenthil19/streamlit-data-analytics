import pandas as pd
import numpy as np
from scipy import stats

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
    """Calculate basic summary statistics with error handling"""
    try:
        # Handle numeric columns
        numeric_cols = get_numeric_columns(df)
        numeric_stats = pd.DataFrame()
        if numeric_cols:
            numeric_stats = df[numeric_cols].describe()

        # Handle categorical columns
        categorical_cols = get_categorical_columns(df)
        categorical_stats = pd.DataFrame()
        if categorical_cols:
            categorical_stats = df[categorical_cols].describe()

        # Calculate missing values
        missing_values = df.isnull().sum()

        return numeric_stats, categorical_stats, missing_values
    except Exception as e:
        raise Exception(f"Error calculating summary statistics: {str(e)}")

def perform_normality_test(data):
    """Perform Shapiro-Wilk normality test"""
    try:
        statistic, p_value = stats.shapiro(data)
        return {
            'test_name': 'Shapiro-Wilk',
            'statistic': statistic,
            'p_value': p_value,
            'is_normal': p_value > 0.05
        }
    except Exception as e:
        return {
            'test_name': 'Shapiro-Wilk',
            'error': str(e)
        }

def perform_ttest(data1, data2=None, paired=False):
    """Perform t-test (one-sample or two-sample)"""
    try:
        if data2 is None:
            # One-sample t-test against mean=0
            statistic, p_value = stats.ttest_1samp(data1, 0)
            test_type = 'One-sample'
        else:
            # Two-sample t-test
            statistic, p_value = stats.ttest_ind(data1, data2) if not paired else stats.ttest_rel(data1, data2)
            test_type = 'Paired' if paired else 'Independent'

        return {
            'test_type': f'{test_type} t-test',
            'statistic': statistic,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    except Exception as e:
        return {
            'test_type': 'T-test',
            'error': str(e)
        }

def perform_anova(data_groups):
    """Perform one-way ANOVA"""
    try:
        f_statistic, p_value = stats.f_oneway(*data_groups)
        return {
            'test_name': 'One-way ANOVA',
            'f_statistic': f_statistic,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    except Exception as e:
        return {
            'test_name': 'ANOVA',
            'error': str(e)
        }

def calculate_effect_size(data1, data2):
    """Calculate Cohen's d effect size"""
    try:
        d = (np.mean(data1) - np.mean(data2)) / np.sqrt(
            ((len(data1) - 1) * np.var(data1) + (len(data2) - 1) * np.var(data2)) /
            (len(data1) + len(data2) - 2)
        )
        return {
            'metric': "Cohen's d",
            'value': d,
            'interpretation': interpret_cohens_d(d)
        }
    except Exception as e:
        return {
            'metric': "Cohen's d",
            'error': str(e)
        }

def interpret_cohens_d(d):
    """Interpret Cohen's d effect size"""
    d = abs(d)
    if d < 0.2:
        return 'Negligible effect'
    elif d < 0.5:
        return 'Small effect'
    elif d < 0.8:
        return 'Medium effect'
    else:
        return 'Large effect'