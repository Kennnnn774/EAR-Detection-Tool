from flask import Flask, request, jsonify
from EAR_Scanner import scan_single_url  # Import your new function
from db import search_for_url, insert_new_document

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan_url():
    url = request.json.get('url')
    exists = search_for_url(url)
    if exists:
        return jsonify(exists)
    else:
        result = scan_single_url(url)
        inserting = insert_new_document(url, result['vulnerable'])
        return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000)