FROM python:3.10-slim

# Install Java (required for Spark)
RUN apt-get update && \
    apt-get install -y default-jdk curl && \
    rm -rf /var/lib/apt/lists/*

# Set Java env
ENV JAVA_HOME=/usr/lib/jvm/default-java

# Install Spark
ENV SPARK_VERSION=3.5.8
ENV HADOOP_VERSION=3

RUN curl -o spark.tgz https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && tar -xzf spark.tgz \
    && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark \
    && rm spark.tgz

ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin

WORKDIR /fastapi

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]