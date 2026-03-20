FROM python:3.12-slim

EXPOSE 8501

WORKDIR /taxi_dash_dir

# copy over requirements
COPY requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything (this includes the 'app' folder)
COPY . .

CMD streamlit run app/main_page_ui.py

