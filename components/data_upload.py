import streamlit as st
from utils import load_data
from database import Dataset, get_session, init_db
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def show_upload_section():
    """
    Display and handle the data upload section of the Streamlit app.
    """
    st.header("Data Upload")
    st.write("Upload your data file (CSV or Excel)")

    try:
        # Initialize database if needed
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        st.error(f"Database initialization error: {str(e)}")
        logger.error(f"Database initialization failed: {str(e)}")
        return

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["csv", "xlsx", "xls"],
        help="Upload a CSV or Excel file"
    )

    if uploaded_file is not None:
        try:
            # Load data into pandas DataFrame
            data = load_data(uploaded_file)
            logger.info(f"Successfully loaded data from {uploaded_file.name}")

            # Store in database
            with get_session() as session:
                dataset = Dataset.from_pandas(data, uploaded_file.name)
                session.add(dataset)
                session.commit()
                logger.info(f"Successfully saved dataset {uploaded_file.name} to database")

                # Store dataset ID in session state
                st.session_state.current_dataset_id = dataset.id
                st.session_state.data = data

            st.success("Data uploaded successfully and saved to database!")
            st.write("Dataset Shape:", data.shape)
            st.write("Preview of the data:")
            st.dataframe(data.head())

        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            logger.error(f"Error processing data: {str(e)}")
            return

    # Show existing datasets
    try:
        with get_session() as session:
            datasets = session.query(Dataset).all()
            if datasets:
                st.subheader("Existing Datasets")
                for dataset in datasets:
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.write(f"Name: {dataset.name}")
                    with col2:
                        st.write(f"Uploaded: {dataset.upload_date.strftime('%Y-%m-%d %H:%M')}")
                    with col3:
                        if st.button("Load", key=f"load_{dataset.id}"):
                            try:
                                data = dataset.to_pandas()
                                st.session_state.current_dataset_id = dataset.id
                                st.session_state.data = data
                                st.success(f"Loaded dataset: {dataset.name}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error loading dataset: {str(e)}")
                                logger.error(f"Error loading dataset {dataset.name}: {str(e)}")
    except Exception as e:
        st.error(f"Error accessing existing datasets: {str(e)}")
        logger.error(f"Error accessing existing datasets: {str(e)}")