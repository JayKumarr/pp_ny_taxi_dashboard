import streamlit as st
import os

from helper import get_parquet_metadata
from nytaxi_logger import get_logger
from request_handler import download_parquet, get_downloaded_files, extract_parquet_data_links

from streamlit_option_menu import option_menu

logger = get_logger(__name__)


st.title('NY Yello Taxi Analysis Dashboard')

# Page config
st.set_page_config(page_title="Home", layout="wide")


dd_page_ = st.Page("pages/dataset_download_ui.py", title="Datasets", icon=":material/database:")

vis_page_ = st.Page("pages/dashboard_ui.py", title="Dashboard", icon=":material/dashboard:")

pg_ = st.navigation({"Main Menu":[dd_page_, vis_page_]})

pg_.run()

# with st.sidebar:
#     selected = option_menu(menu_title="Main Manu",
#                            options=["Datasets", "Visualization", "Data Processing"],
#                            icons=["database", "bar_chart","graph_3"],
#                            menu_icon="cast"
#                            )


