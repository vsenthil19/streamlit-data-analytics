import streamlit as st
import pandas as pd
from components.data_upload import show_upload_section
from components.data_explorer import show_explorer_section
from components.visualizations import show_visualization_section
from components.analysis import show_analysis_section

st.set_page_config(
    page_title="Data Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title("📊 Interactive Data Analytics Dashboard")
    
    st.sidebar.header("Navigation")
    page = st.sidebar.radio(
        "Select a Section:",
        ["Data Upload", "Data Explorer", "Visualizations", "Analysis"]
    )
    
    # Initialize session state for data storage
    if 'data' not in st.session_state:
        st.session_state.data = None
    
    if page == "Data Upload":
        show_upload_section()
    elif page == "Data Explorer":
        if st.session_state.data is not None:
            show_explorer_section(st.session_state.data)
        else:
            st.warning("Please upload data first!")
    elif page == "Visualizations":
        if st.session_state.data is not None:
            show_visualization_section(st.session_state.data)
        else:
            st.warning("Please upload data first!")
    elif page == "Analysis":
        if st.session_state.data is not None:
            show_analysis_section(st.session_state.data)
        else:
            st.warning("Please upload data first!")

if __name__ == "__main__":
    main()
