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

    try:
        payload = json.dumps({
            "collection": "WSFinal",
            "database": "WSFinal",
            "dataSource": "WebSecurityFinal",
            "filter": {
                "url": url
            }
        })
        response = requests.request("POST", dest, headers=headers, data=payload)
        status_code = response.status_code
        response = response.json()
        response = response['document']
        if response:
            response['status_code'] = status_code
        return response
    except Exception as err:
        print(err)
        return {
            "url": url,
            "err": str(err)
        }

# insert new results for a specified url
def insert_new_document(url, result, message):
    dest = os.getenv('DB_URL_API_BASE') + "insertOne"
    dateChecked = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    
    try:
        payload = json.dumps({
            "collection": "WSFinal",
            "database": "WSFinal",
            "dataSource": "WebSecurityFinal",
            "document": {
                "url": url,
                "vulnerable": result,
                "dateChecked": dateChecked,
                "message": message
            }
        })
        response = requests.request("POST", dest, headers=headers, data=payload)
        response = response.json()
        response['dateChecked'] = dateChecked
        return response
    except Exception as err:
        print(err)
        return {
            "url": url,
            "err": str(err)
        }