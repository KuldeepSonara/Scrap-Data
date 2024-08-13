import requests
import json
url = "https://www2.daad.de/deutschland/studienangebote/international-programmes/api/solr/en/search.json"
params = {
    "cert": "",
    "admReq": "",
    "langExamPC": "",
    "scholarshipLC": "",
    "langExamLC": "",
    "scholarshipSC": "",
    "langExamSC": "",
    "fos": "",
    "langDeAvailable": "",
    "langEnAvailable": "",
    "fee": "",
    "sort": "4",
    "dur": "",
    "q": "",
    "limit": "3000",
    "offset": "10",
    "display": "list",
    "isElearning": "",
    "isSep": ""
}

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print(len(data["courses"]))
    with open('./daad_data.json', 'w') as json_file:
        json.dump(response.json(), json_file, indent=4)
    print("Data saved to daad_data.json")
    # print(data)  # or process the data as needed
else:
    print(f"Error: {response.status_code} - {response.text}")
