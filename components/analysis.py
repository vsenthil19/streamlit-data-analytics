import streamlit as st
import pandas as pd
import numpy as np
from utils import get_numeric_columns

def show_analysis_section(df):
    st.header("Data Analysis")
    
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Correlation Analysis", "Basic Statistics", "Group Analysis"]
    )
    
    if analysis_type == "Correlation Analysis":
        numeric_cols = get_numeric_columns(df)
        
        # Correlation matrix
        corr_matrix = df[numeric_cols].corr()
        
        st.subheader("Correlation Matrix")
        st.dataframe(corr_matrix.style.background_gradient(cmap='RdBu', vmin=-1, vmax=1))
        
        # Correlation heatmap
        import plotly.graph_objects as go
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmin=-1,
            zmax=1
        ))
        fig.update_layout(title="Correlation Heatmap")
        st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Basic Statistics":
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Central Tendency")
            st.dataframe(df.agg(['mean', 'median', 'mode']).T)
        
        with col2:
            st.subheader("Dispersion")
            st.dataframe(df.agg(['std', 'var', 'min', 'max']).T)
    
    elif analysis_type == "Group Analysis":
        numeric_cols = get_numeric_columns(df)
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        if len(categorical_cols) > 0:
            group_col = st.selectbox("Group by", categorical_cols)
            agg_col = st.selectbox("Select column to aggregate", numeric_cols)
            agg_func = st.selectbox(
                "Select aggregation function",
                ["mean", "sum", "count", "min", "max"]
            )
            
            grouped_data = df.groupby(group_col)[agg_col].agg(agg_func)
            
            st.subheader(f"{agg_func.capitalize()} of {agg_col} by {group_col}")
            st.dataframe(grouped_data)
            
            # Visualization of grouped data
            fig = go.Figure(data=go.Bar(
                x=grouped_data.index,
                y=grouped_data.values
            ))
            fig.update_layout(
                title=f"{agg_func.capitalize()} of {agg_col} by {group_col}",
                xaxis_title=group_col,
                yaxis_title=f"{agg_func.capitalize()} of {agg_col}"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No categorical columns available for grouping.")
