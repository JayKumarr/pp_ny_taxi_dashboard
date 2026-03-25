from fastapi import FastAPI
import subprocess
from pathlib import Path

from rest_logger import get_logger

app = FastAPI()

SPARK_MASTER = "spark://spark-master:7077"

logger_ = get_logger(__name__)

@app.get("/")
def read_root():
    log_path_ = "logs/"
    return {"status": f"FastAPI is running inside Docker!"}
@app.get("/run-job")
def run_spark_job():
    try:
        # logger.info("received request..")
        result = subprocess.run(
            ["docker",
                "exec",
                "spark-master",
                "/opt/spark/bin/spark-submit",
                "--master",
                SPARK_MASTER,
                "/opt/spark-apps/process_parquet_job.py",
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