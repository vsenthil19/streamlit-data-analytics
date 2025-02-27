import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import get_numeric_columns, get_categorical_columns

def show_visualization_section(df):
    st.header("Data Visualizations")
    
    # Get columns by type
    numeric_cols = get_numeric_columns(df)
    categorical_cols = get_categorical_columns(df)
    
    # Chart type selector
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Scatter Plot", "Bar Chart", "Line Chart", "Box Plot", "Histogram"]
    )
    
    if chart_type == "Scatter Plot":
        x_col = st.selectbox("Select X-axis", numeric_cols, key="scatter_x")
        y_col = st.selectbox("Select Y-axis", numeric_cols, key="scatter_y")
        color_col = st.selectbox("Color by (optional)", ["None"] + categorical_cols)
        
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=None if color_col == "None" else color_col,
            title=f"Scatter Plot: {y_col} vs {x_col}"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Bar Chart":
        x_col = st.selectbox("Select X-axis", categorical_cols, key="bar_x")
        y_col = st.selectbox("Select Y-axis", numeric_cols, key="bar_y")
        
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            title=f"Bar Chart: {y_col} by {x_col}"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Line Chart":
        x_col = st.selectbox("Select X-axis", numeric_cols, key="line_x")
        y_col = st.selectbox("Select Y-axis", numeric_cols, key="line_y")
        
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            title=f"Line Chart: {y_col} vs {x_col}"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Box Plot":
        y_col = st.selectbox("Select Variable", numeric_cols, key="box_y")
        x_col = st.selectbox("Group by (optional)", ["None"] + categorical_cols)
        
        fig = px.box(
            df,
            y=y_col,
            x=None if x_col == "None" else x_col,
            title=f"Box Plot: {y_col}"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Histogram":
        col = st.selectbox("Select Variable", numeric_cols, key="hist_x")
        bins = st.slider("Number of bins", 5, 100, 30)
        
        fig = px.histogram(
            df,
            x=col,
            nbins=bins,
            title=f"Histogram: {col}"
        )
        st.plotly_chart(fig, use_container_width=True)
