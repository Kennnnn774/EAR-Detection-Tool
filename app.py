from flask import Flask, request, jsonify
from EAR_Scanner import scan_single_url  # Import your new function

app = Flask(__name__)

@app.route('/')
def EAR():
    return 'Hello, World!'

@app.route('/scan', methods=['POST'])
def scan_url():
    url = request.json.get('url')
    result = scan_single_url(url)
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000)