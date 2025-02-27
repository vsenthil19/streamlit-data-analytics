import streamlit as st
from utils import get_numeric_columns, get_categorical_columns, calculate_summary_stats

def show_explorer_section(df):
    st.header("Data Explorer")
    
    # Basic information
    st.subheader("Dataset Information")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())
    
    # Summary statistics
    st.subheader("Summary Statistics")
    numeric_stats, categorical_stats, missing_values = calculate_summary_stats(df)
    
    tab1, tab2, tab3 = st.tabs(["Numeric Stats", "Categorical Stats", "Missing Values"])
    
    with tab1:
        st.dataframe(numeric_stats)
    
    with tab2:
        st.dataframe(categorical_stats)
    
    with tab3:
        st.dataframe(missing_values.to_frame(name='Missing Values'))
    
    # Data viewer with filters
    st.subheader("Data Viewer")
    
    # Column selector
    selected_columns = st.multiselect(
        "Select columns to view",
        df.columns.tolist(),
        default=df.columns.tolist()
    )
    
    # Sorting
    sort_column = st.selectbox("Sort by column", selected_columns)
    sort_order = st.radio("Sort order", ["Ascending", "Descending"])
    
    # Filter data
    filtered_df = df[selected_columns].sort_values(
        by=sort_column,
        ascending=(sort_order == "Ascending")
    )
    
    st.dataframe(filtered_df)
