import requests
import json


API_URL = "https://grg7og4c2d.execute-api.us-east-1.amazonaws.com/prod/ingest"


def send_report(report):
    headers = {"Content-Type": "application/json"}

    response = requests.post(API_URL, headers=headers, data=json.dumps(report))

    if response.status_code == 200:
        return True, response.text
    else:
        return False, response.text
