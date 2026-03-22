import os

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json
from datetime import date, datetime
from collections import defaultdict

from nytaxi_logger import get_logger


logger = get_logger(__name__)

# Get the absolute path of the current file
current_file = Path(__file__).resolve().parent
# to store data, metadata
DATA_DIR_ = Path.joinpath(current_file.parent, "data")

# This file has all links of parquest file data
LINKS_JSON_FILE = Path.joinpath(DATA_DIR_, "all_links.json")

NY_TAXI_ENDPOINT =  "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
def get_all_parquet_files() -> list:
    response = requests.get(NY_TAXI_ENDPOINT)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        exit_links = soup.find_all('a', title="Yellow Taxi Trip Records")
        return exit_links

    return []

def prepare_data_link_dic(href_list: list) -> dict:
    dict__ = defaultdict(list)
    for htag_ in href_list:
        href = htag_.get('href')
        dict__[htag_.text].append(href.strip())

    return dict__

def extract_parquet_data_links() -> dict:
    try:
        if LINKS_JSON_FILE.exists() and is_recently_updated():
            with open(LINKS_JSON_FILE,"r")  as fo:
                json_d = json.load(fo)
                return json_d

        else:
            tags_ = get_all_parquet_files()
            data = prepare_data_link_dic(tags_)
            # Writing to a file
            with open(LINKS_JSON_FILE, 'w') as f:
                json.dump(data, f)

            return data
    except Exception as e:
        logger.error(f"extracting parquet data links failed: {e}")
        return {}


def is_recently_updated() -> bool:
    mtime = LINKS_JSON_FILE.stat().st_mtime
    modification_date = datetime.fromtimestamp(mtime).date()
    if modification_date == date.today():
        return True

    return False

def get_downloaded_files()-> list:
    prq_files = list(DATA_DIR_.glob('*.parquet'))
    return prq_files


def download_parquet(url, save_path=DATA_DIR_) ->  bool:
    try:
        response = requests.get(url, stream=True)
        file_name = os.path.basename(url)
        # Raise an error if the request was unsuccessful (e.g., 404 or 500)
        response.raise_for_status()

        # Open the local file in 'write binary' mode
        with open(os.path.join(save_path,file_name), 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")

    return False

if __name__ == '__main__':
    links_ = extract_parquet_data_links()
    a = 10

