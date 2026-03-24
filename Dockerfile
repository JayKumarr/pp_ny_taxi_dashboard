FROM python:3-slim

# Switch to root to install requirements and set permissions
USER root

WORKDIR /taxi_dash_dir

# copy over requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# Copy everything (this includes the 'app' folder)
COPY . .

EXPOSE 8501

CMD streamlit run app/main_page_ui.py