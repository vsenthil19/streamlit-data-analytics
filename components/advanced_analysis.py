import streamlit as st
import pandas as pd
import numpy as np
from utils import (
    get_numeric_columns,
    get_categorical_columns,
    perform_normality_test,
    perform_ttest,
    perform_anova,
    calculate_effect_size
)
import plotly.figure_factory as ff
import plotly.express as px

def show_advanced_analysis_section(df):
    st.header("Advanced Statistical Analysis")
    
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Distribution Analysis", "Hypothesis Testing", "Effect Size Analysis"]
    )
    
    if analysis_type == "Distribution Analysis":
        show_distribution_analysis(df)
    elif analysis_type == "Hypothesis Testing":
        show_hypothesis_testing(df)
    else:
        show_effect_size_analysis(df)

def show_distribution_analysis(df):
    st.subheader("Distribution Analysis")
    
    numeric_cols = get_numeric_columns(df)
    if not numeric_cols:
        st.warning("No numeric columns available for analysis.")
        return
    
    selected_col = st.selectbox(
        "Select column for distribution analysis",
        numeric_cols
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histogram with KDE
        fig = ff.create_distplot(
            [df[selected_col].dropna()],
            [selected_col],
            show_hist=True,
            show_rug=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Q-Q plot
        fig = px.scatter(
            x=np.sort(df[selected_col].dropna()),
            y=stats.norm.ppf(np.linspace(0.01, 0.99, len(df[selected_col].dropna()))),
            labels={'x': 'Sample Quantiles', 'y': 'Theoretical Quantiles'},
            title='Q-Q Plot'
        )
        fig.add_shape(
            type='line',
            x0=df[selected_col].min(),
            y0=stats.norm.ppf(0.01),
            x1=df[selected_col].max(),
            y1=stats.norm.ppf(0.99),
            line=dict(color='red', dash='dash')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Normality test results
    normality_results = perform_normality_test(df[selected_col].dropna())
    st.subheader("Normality Test Results")
    if 'error' in normality_results:
        st.error(f"Error performing normality test: {normality_results['error']}")
    else:
        st.write(f"Test: {normality_results['test_name']}")
        st.write(f"Statistic: {normality_results['statistic']:.4f}")
        st.write(f"P-value: {normality_results['p_value']:.4f}")
        st.write(f"Conclusion: {'Normal distribution' if normality_results['is_normal'] else 'Not normally distributed'}")

def show_hypothesis_testing(df):
    st.subheader("Hypothesis Testing")
    
    test_type = st.selectbox(
        "Select Test Type",
        ["One-sample t-test", "Two-sample t-test", "Paired t-test", "One-way ANOVA"]
    )
    
    numeric_cols = get_numeric_columns(df)
    categorical_cols = get_categorical_columns(df)
    
    if test_type == "One-sample t-test":
        selected_col = st.selectbox("Select column", numeric_cols)
        if selected_col:
            results = perform_ttest(df[selected_col].dropna())
            display_test_results(results)
    
    elif test_type in ["Two-sample t-test", "Paired t-test"]:
        col1 = st.selectbox("Select first column", numeric_cols, key="col1")
        col2 = st.selectbox("Select second column", numeric_cols, key="col2")
        if col1 and col2:
            results = perform_ttest(
                df[col1].dropna(),
                df[col2].dropna(),
                paired=(test_type == "Paired t-test")
            )
            display_test_results(results)
    
    elif test_type == "One-way ANOVA":
        if not categorical_cols:
            st.warning("No categorical columns available for grouping.")
            return
        
        group_col = st.selectbox("Select grouping column", categorical_cols)
        value_col = st.selectbox("Select value column", numeric_cols)
        
        if group_col and value_col:
            groups = [group.values for name, group in df.groupby(group_col)[value_col]]
            results = perform_anova(groups)
            display_test_results(results)

def show_effect_size_analysis(df):
    st.subheader("Effect Size Analysis")
    
    numeric_cols = get_numeric_columns(df)
    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns for effect size analysis.")
        return
    
    col1 = st.selectbox("Select first column", numeric_cols, key="effect_col1")
    col2 = st.selectbox("Select second column", numeric_cols, key="effect_col2")
    
    if col1 and col2:
        results = calculate_effect_size(
            df[col1].dropna(),
            df[col2].dropna()
        )
        if 'error' in results:
            st.error(f"Error calculating effect size: {results['error']}")
        else:
            st.write(f"Effect Size ({results['metric']}): {results['value']:.4f}")
            st.write(f"Interpretation: {results['interpretation']}")

def display_test_results(results):
    if 'error' in results:
        st.error(f"Error performing test: {results['error']}")
        return
    
    st.write(f"Test: {results.get('test_type', results.get('test_name', 'Statistical Test'))}")
    if 'f_statistic' in results:
        st.write(f"F-statistic: {results['f_statistic']:.4f}")
    if 'statistic' in results:
        st.write(f"Test statistic: {results['statistic']:.4f}")
    st.write(f"P-value: {results['p_value']:.4f}")
    st.write(f"Result: {'Significant' if results['significant'] else 'Not significant'} at α=0.05")
