from flask import Flask, request, jsonify
from EAR_Scanner import scan_single_url  # Import your new function
from flask_cors import CORS
from db import search_for_url, insert_new_document
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

@app.route('/')
def EAR():
    return 'Hello, World!'

@app.route('/scan', methods=["POST"])
def scan_url():
    url = request.json.get('url')
    exists = search_for_url(url)

    if exists:
        #if error is returned return that error
        if exists.get('err'):
            return jsonify(exists)

        #if entry exists in database with this url, then check when it was last updated
        date = datetime.strptime(exists['dateChecked'], "%m/%d/%Y, %H:%M:%S")
        date_plus_week = date + timedelta(days=7)
        today = datetime.now()

        #Will update if last updated more than a week ago
        if date_plus_week < today:
            result = scan_single_url(url)
            inserting = insert_new_document(url, result['vulnerable'], result['message'])

            #if error is returned, return that error
            if inserting.get('err'):
                return jsonify(inserting)
            else:
                result['dateChecked'] = inserting['dateChecked']
                result['_id'] = inserting['insertedId']
                return jsonify(result)
        else:
            return jsonify(exists)
    else:
        #Create new entry in database because no previous entry existed
        result = scan_single_url(url)
        inserting = insert_new_document(url, result['vulnerable'], result['message'])
        
        #if error is returned, return that error
        if inserting.get('err'):
            return jsonify(inserting)
        else:
            result['dateChecked'] = inserting['dateChecked']
            result['_id'] = inserting['insertedId']
            return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000)