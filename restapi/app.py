from fastapi import FastAPI
import subprocess
from pyspark.sql import SparkSession

from rest_logger import get_logger

app = FastAPI()

SPARK_MASTER = "spark://spark-master:7077"

logger_ = get_logger(__name__)

@app.get("/")
def read_root():
    return {"status": f"FastAPI is running inside Docker!"}

@app.get("/run-job")
def run_spark_job():
    logger_.info("received request for run job")
    # try:
    #     spark = SparkSession.builder \
    #         .master(SPARK_MASTER) \
    #         .appName("MyRemoteApp") \
    #         .getOrCreate()
    #
    #     logger_.info(f"succesfully created spark: {spark}")
    #     spark.stop()
    # except Exception as e:
    #     logger_.error(f"Something failed : {e}")


    try:
        result = subprocess.run(
            [
                "/opt/spark/bin/spark-submit",
                "--master",
                SPARK_MASTER,
                "/opt/spark/jobs/process_parquet_job.py",
            ],
            capture_output=True,
            text=True,
        )

        return {
            "status": "success",
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}