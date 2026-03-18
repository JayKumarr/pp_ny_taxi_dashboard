FROM python:3.12-slim

EXPOSE 8501

WORKDIR /ny-txi-app

# copy over requirements
COPY requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything (this includes the 'app' folder)
COPY . .

CMD streamlit run app/streamlit_app.py

# ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]