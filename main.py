import streamlit as st
import pandas as pd
import logging
from components.data_upload import show_upload_section
from components.data_explorer import show_explorer_section
from components.visualizations import show_visualization_section
from components.analysis import show_analysis_section
from components.advanced_analysis import show_advanced_analysis_section
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables at startup
try:
    load_dotenv()
    logger.info("Environment variables loaded successfully")
    if os.getenv("DATABASE_URL"):
        logger.info("DATABASE_URL found in environment")
    else:
        logger.error("DATABASE_URL not found in environment")
except Exception as e:
    logger.error(f"Error loading environment variables: {str(e)}")

try:
    st.set_page_config(
        page_title="Data Analytics Dashboard",
        page_icon="📊",
        layout="wide"
    )
    logger.info("Page configuration set successfully")
except Exception as e:
    logger.error(f"Error setting page configuration: {str(e)}")
    raise

def main():
    try:
        st.title("📊 Interactive Data Analytics Dashboard")
        logger.info("Main dashboard initialized")

        st.sidebar.header("Navigation")
        page = st.sidebar.radio(
            "Select a Section:",
            ["Data Upload", "Data Explorer", "Visualizations", "Analysis", "Advanced Analysis"]
        )

        # Initialize session state for data storage
        if 'data' not in st.session_state:
            st.session_state.data = None
            logger.info("Session state initialized")

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
        elif page == "Advanced Analysis":
            if st.session_state.data is not None:
                show_advanced_analysis_section(st.session_state.data)
            else:
                st.warning("Please upload data first!")

        logger.info(f"Successfully rendered {page} section")

    except Exception as e:
        logger.error(f"Error in main application: {str(e)}")
        st.error("An error occurred in the application. Please try again.")

if __name__ == "__main__":
    try:
        logger.info("Starting Streamlit application")
        main()
        logger.info("Application running successfully")
    except Exception as e:
        logger.error(f"Application startup error: {str(e)}")
        st.error("Failed to start the application. Please check the logs.")