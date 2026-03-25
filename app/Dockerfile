FROM python:3.10-slim

# Switch to root to install requirements and set permissions
USER root

WORKDIR /taxi_dash_dir

# copy over requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD streamlit run ui_home_page.py