import streamlit as st
from utils import load_data

def show_upload_section():
    st.header("Data Upload")
    st.write("Upload your data file (CSV or Excel)")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["csv", "xlsx", "xls"],
        help="Upload a CSV or Excel file"
    )
    
    if uploaded_file is not None:
        try:
            data = load_data(uploaded_file)
            st.session_state.data = data
            
            st.success("Data uploaded successfully!")
            st.write("Dataset Shape:", data.shape)
            st.write("Preview of the data:")
            st.dataframe(data.head())
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
