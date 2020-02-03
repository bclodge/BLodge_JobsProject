import requests
import json


# get jobs is taking url from main, sending request to site and checking status code before "prettying" json data.
def check_jobs():
    with open('gitjob.txt') as data:
        if "Senior Mobile Developer" in data.read():
            print("true")
        else:
            print("false! not found.")


def get_jobs(url):
    r = requests.get(url)

    if r.status_code == 200:
        pretty_json = json.loads(r.text)
        print(len(pretty_json))
        save_to_file(pretty_json)
    else:
        print(r.status_code)

# save_to_file is called by get_jobs, passing in cleaned up json data, then doing name.

def save_to_file(pretty_json):
    with open('gitjob.txt', 'w') as outfile:
        outfile.write(json.dumps(pretty_json, indent=2))
    outfile.close()


# f string handles pagination for jobs.
def main():
    for i in range(1, 6):
        url = f"https://jobs.github.com/positions.json?page={i}"
        get_jobs(url)


# main()
