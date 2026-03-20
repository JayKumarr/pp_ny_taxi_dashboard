import streamlit as st
import os

from helper import get_parquet_metadata
from nytaxi_logger import get_logger
from request_handler import download_parquet, get_downloaded_files, extract_parquet_data_links

logger = get_logger(__name__)

# 1. Initialize the 'processing' state
if 'processing' not in st.session_state:
    st.session_state.processing = False

def start_processing():
    st.session_state.processing = True

st.title('NY Yello Taxi Analysis Dashboard')

# Page config
st.set_page_config(page_title="Dashboard", layout="wide")

# Sample options for the searchable selection box
links_  = extract_parquet_data_links()
options = links_[list(links_.keys())[0]]  # list of links



# Header section with 3 tabs
tab1, tab2, tab3 = st.tabs(["Download", "Statistics", "Analyze"])

options = {os.path.basename(url):url for url in options}
# Main body split into 25% and 75%
left_col, right_col = st.columns([1, 3])


downloaded_file_dict_ = get_parquet_metadata(get_downloaded_files())

with left_col:
    st.subheader("Search / Select")
    selected_item = st.selectbox(
        label="Choose an option",
        options=options.keys(),
        index=None,
        placeholder="Search and select...",
        key='data_search_box'
    )
    download_btn = st.button("Download",
                             key='download_btn',
                             icon=":material/download:",
                             on_click = start_processing,
                             disabled = st.session_state.processing
    )



with right_col:
    status_placeholder = st.empty()
    # product_data = {
    #     "Files": [
    #         ":material/devices: Widget Pro",
    #         ":material/smart_toy: Smart Device",
    #         ":material/inventory: Premium Kit",
    #     ],
    #     "Size": [":blue[Electronics]", ":green[IoT]", ":violet[Bundle]"]
    # }
    dataset_table = st.table(downloaded_file_dict_)

    if download_btn:
        if selected_item:
            with st.spinner("Downloading..."):
                try:
                    success_ = download_parquet(options[selected_item] )
                    if success_:
                        downloaded_ = get_parquet_metadata(get_downloaded_files())
                        dataset_table.table(downloaded_)
                finally:
                    st.session_state.processing = False
                    st.rerun()


# Tab content
with tab1:
    st.write("This is the Download tab content.")

with tab2:
    st.write("This is the Statistics tab content.")

with tab3:
    st.write("This is the Analyze tab content.")


