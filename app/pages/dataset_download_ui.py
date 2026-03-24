import streamlit as st
import os

from helper import get_parquet_metadata, logger
from request_handler import extract_parquet_data_links, get_downloaded_files, download_parquet

st.set_page_config(page_title="Download Dataset", page_icon=":material/database:")

left_col, right_col = st.columns([1, 3])


# 1. Initialize the 'processing' state
if 'processing' not in st.session_state:
    st.session_state.processing = False

def start_processing():
    st.session_state.processing = True

# Sample options for the searchable selection box
links_  = extract_parquet_data_links()
dataset_links_options = links_[list(links_.keys())[0]]  # list of links
dataset_links_options = {os.path.basename(url):url for url in dataset_links_options}
# Main body split into 25% and 75%



downloaded_file_dict_ = get_parquet_metadata(get_downloaded_files())


with left_col:
    st.subheader("Search / Select")
    selected_item = st.selectbox(
        label="Choose an option",
        options=dataset_links_options.keys(),
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
    dataset_table = st.table(downloaded_file_dict_)

    if download_btn:
        if selected_item:
            with st.spinner("Downloading..."):
                try:
                    success_ = download_parquet(dataset_links_options[selected_item])
                    if success_:
                        downloaded_ = get_parquet_metadata(get_downloaded_files())
                        dataset_table.table(downloaded_)
                except Exception as e:
                    logger.error(f"Failed: {e}")
                finally:
                    st.session_state.processing = False
                    st.rerun()

@st.dialog("Cast your vote")
def vote(item):
    st.write(f"Why is {item} your favorite?")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()

if "vote" not in st.session_state:
    st.write("Vote for your favorite")
    if st.button(str("A")):
        vote("A")
    if st.button("B"):
        vote("B")

