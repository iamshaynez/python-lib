# This code sample uses the 'requests' library:
import requests

url = "https://data.mixpanel.com/api/2.0/nessie/pipeline/create"

payload = {
    "type": "gcs-raw",
    "trial": False,
    "data_source": "events",
    "frequency": "daily",
    "data_format": "json",
    "gcs_region": "northamerica-northeast1"
}
headers = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=payload, headers=headers)

print(response.text)