import requests
import time
from typing import Dict,List
import _sqlite3


# get jobs is taking url from main, sending request to site and checking status code before "prettying" json data.
def check_jobs():
    with open('gitjob.txt') as data:
        if "Senior Mobile Developer" in data.read():
            print("true")
        else:
            print("false! not found.")


def get_jobs() -> List[Dict]:

    all_job_data = []
    numOfPages = 1
    isThereMorePages = True;

    while isThereMorePages:
        url = f"https://jobs.github.com/positions.json?page={numOfPages}"
        Requested_data = requests.get(url)

        job_list_json = Requested_data.json()

        all_job_data.extend(job_list_json)

        if len(job_list_json) < 50:
            isThereMorePages = False
        time.sleep(.1)  # give it a little nap
        numOfPages += 1

    return all_job_data


def save_to_file(data, filename = 'gitjob.txt'):
    with open('gitjob.txt', 'a') as outfile:
        for line_items in data:
            print(line_items, file=outfile)


def main():
    target_data = get_jobs()
    save_to_file(target_data)
