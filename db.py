import datetime
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# x = datetime.datetime.now()
# print(x)
# datetime.strptime() method to convert from string to datetime object
# datetime.strftime() method to convert from object to string, with arguments to specify info needed

headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': os.getenv('DB_API_KEY'),
}


# search for db records based on a given url
# returns None if none found
def search_for_url(url):
    dest = "https://us-east-2.aws.data.mongodb-api.com/app/data-kkxqh/endpoint/data/v1/action/findOne"
    payload = json.dumps({
        "collection": "Web Security final",
        "database": "WSFinal",
        "dataSource": "WebSecurityFinal",
        "filter": {
            "url": url
        }
    })

    try:
        response = requests.request("POST", dest, headers=headers, data=payload)
        status_code = response.status_code
        response = response.json()
        response = response['document']

        if response['result']:
            # vulnerable
            return {'vulnerable': response['result'], 'url': response['url'], 'dateChecked': response['dateChecked'], "message": 'Redirect found. Vulnerable.', "status_code": status_code}

        else:
            return {'vulnerable': response['result'], 'url': response['url'], 'dateChecked': response['dateChecked'], "message": 'No redirect found. Not vulnerable.', "status_code": status_code}
    except Exception as err:
        print(err)

# insert new results for a specified url
def insert_new_document(url, result):
    dest = "https://us-east-2.aws.data.mongodb-api.com/app/data-kkxqh/endpoint/data/v1/action/insertOne"
    payload = json.dumps({
        "collection": "Web Security final",
        "database": "WSFinal",
        "dataSource": "WebSecurityFinal",
        "document": {
            "url": url,
            "result": result,
            "dateChecked": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        }
    })
    try:
        response = requests.request("POST", dest, headers=headers, data=payload)
        response = response.json()
        return response
    except Exception as err:
        print(err)