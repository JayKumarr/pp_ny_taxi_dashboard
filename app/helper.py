import os
import pyarrow.parquet as pq

from nytaxi_logger import get_logger

logger = get_logger(__name__)

def get_parquet_metadata(file_paths:list ) -> dict:
    # Initialize the dictionary structure
    data_dict = {
        "file_name": [],
        "file_size": [],
        "total_records": []
    }

    for path in file_paths:
        if os.path.exists(path):
            # 1. Get the file name from the path
            data_dict["file_name"].append(os.path.basename(path))

            # 2. Get file size in MB (rounded to 2 decimal places)
            size_bytes = os.path.getsize(path)
            size_mb = round(size_bytes / (1024 * 1024), 2)
            data_dict["file_size"].append(f"{size_mb} MB")

            # 3. Get total records from Parquet metadata (very fast)
            parquet_file = pq.ParquetFile(path)
            data_dict["total_records"].append(parquet_file.metadata.num_rows)
        else:
            logger.error(f"Path not found {path}")

    return data_dict
