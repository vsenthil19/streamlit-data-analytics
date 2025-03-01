import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils import get_numeric_columns

def show_analysis_section(df):
    st.header("Data Analysis")

    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Correlation Analysis", "Basic Statistics", "Group Analysis"]
    )

    if analysis_type == "Correlation Analysis":
        numeric_cols = get_numeric_columns(df)

        if len(numeric_cols) < 2:
            st.warning("Need at least 2 numeric columns for correlation analysis.")
            return

        try:
            # Correlation matrix calculation
            corr_matrix = df[numeric_cols].corr()

            # Display correlation matrix as a table
            st.subheader("Correlation Matrix")
            st.dataframe(corr_matrix.round(3))

            # Correlation heatmap using plotly
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmin=-1,
                zmax=1
            ))

            fig.update_layout(
                title="Correlation Heatmap",
                width=700,
                height=700,
                xaxis_title="Features",
                yaxis_title="Features"
            )

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error in correlation analysis: {str(e)}")
            return

    elif analysis_type == "Basic Statistics":
        try:
            numeric_cols = get_numeric_columns(df)
            if not numeric_cols:
                st.warning("No numeric columns found for statistical analysis.")
                return

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Central Tendency")
                central_tendency = df[numeric_cols].agg(['mean', 'median']).round(3)
                st.dataframe(central_tendency)

            with col2:
                st.subheader("Dispersion")
                dispersion = df[numeric_cols].agg(['std', 'min', 'max']).round(3)
                st.dataframe(dispersion)

        except Exception as e:
            st.error(f"Error in basic statistics calculation: {str(e)}")
            return

    elif analysis_type == "Group Analysis":
        try:
            numeric_cols = get_numeric_columns(df)
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns

            if len(categorical_cols) == 0:
                st.warning("No categorical columns available for grouping.")
                return

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
                yaxis_title=f"{agg_func.capitalize()} of {agg_col}",
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error in group analysis: {str(e)}")
            return