import streamlit as st

# Page config
st.set_page_config(page_title="Home", layout="wide")


dd_page_ = st.Page("pages/dataset_download_ui.py", title="Datasets", icon=":material/database:")

vis_page_ = st.Page("pages/dashboard_ui.py", title="Dashboard", icon=":material/dashboard:")

pg_ = st.navigation({"Main Menu":[dd_page_, vis_page_]})

pg_.run()



