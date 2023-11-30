import datetime
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': os.getenv('DB_API_KEY'),
}


# search for db records based on a given url
# returns None if none found
def search_for_url(url):
    dest = os.getenv('DB_URL_API_BASE') + "findOne"
    payload = json.dumps({
        "collection": "WSFinal",
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
        response['status_code'] = status_code
        return response
    except Exception as err:
        print(err)
        return {
            "url": url,
            "err": err
        }

# insert new results for a specified url
def insert_new_document(url, result, message):
    dest = os.getenv('DB_URL_API_BASE') + "insertOne"
    payload = json.dumps({
        "collection": "WSFinal",
        "database": "WSFinal",
        "dataSource": "WebSecurityFinal",
        "document": {
            "url": url,
            "vulnerable": result,
            "dateChecked": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "message": message
        }
    })
    try:
        response = requests.request("POST", dest, headers=headers, data=payload)
        response = response.json()
        return response
    except Exception as err:
        print(err)
        return {
            "url": url,
            "err": err
        }