from flask import Flask, request, jsonify
from utils import extract_signature

app = Flask(__name__)

@app.route('/extract-signature', methods=['POST'])
def extract_sign():
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF uploaded"}), 400
    
    file = request.files['pdf']
    result = extract_signature(file)
    return jsonify(result)
