import streamlit as st
import pandas as pd
from utils import get_numeric_columns, get_categorical_columns, calculate_summary_stats

def show_explorer_section(df):
    """Display and handle the data explorer section of the Streamlit app."""
    try:
        st.header("Data Explorer")

        # Basic information
        st.subheader("Dataset Information")
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", df.isnull().sum().sum())

        # Summary statistics
        st.subheader("Summary Statistics")
        try:
            numeric_stats, categorical_stats, missing_values = calculate_summary_stats(df)

            tab1, tab2, tab3 = st.tabs(["Numeric Stats", "Categorical Stats", "Missing Values"])

            with tab1:
                if not numeric_stats.empty:
                    st.dataframe(numeric_stats)
                else:
                    st.info("No numeric columns found in the dataset.")

            with tab2:
                if not categorical_stats.empty:
                    st.dataframe(categorical_stats)
                else:
                    st.info("No categorical columns found in the dataset.")

            with tab3:
                missing_df = missing_values.to_frame(name='Missing Values')
                if not missing_df.empty:
                    st.dataframe(missing_df)
                else:
                    st.info("No missing values found in the dataset.")

        except Exception as e:
            st.error(f"Error calculating summary statistics: {str(e)}")

        # Data viewer with filters
        st.subheader("Data Viewer")

        # Column selector
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect(
            "Select columns to view",
            all_columns,
            default=all_columns
        )

        if not selected_columns:
            st.warning("Please select at least one column to view the data.")
            return

        # Sorting
        sort_column = st.selectbox("Sort by column", selected_columns)
        sort_order = st.radio("Sort order", ["Ascending", "Descending"])

        try:
            # Filter data
            filtered_df = df[selected_columns].sort_values(
                by=sort_column,
                ascending=(sort_order == "Ascending")
            )

            # Show row count
            st.write(f"Showing {len(filtered_df)} rows")

            # Display the dataframe
            st.dataframe(filtered_df)

        except Exception as e:
            st.error(f"Error processing data: {str(e)}")

    except Exception as e:
        st.error(f"Error in data explorer: {str(e)}")