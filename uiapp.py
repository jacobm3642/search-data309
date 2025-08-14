from flask import Flask, render_template, request, jsonify
import requests
import os
import random

app = Flask(__name__)

# Pinecone settings
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_URL = "https://semantic-search-ngjtb5f.svc.aped-4627-b74a.pinecone.io"
VECTOR_DIM = 1024
placeholder_vector = [random.uniform(0.01, 0.1) for _ in range(VECTOR_DIM)]

# Serverless upsert endpoint
UPSERT_URL = f"{PINECONE_URL}/vectors/upsert"

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/send-query', methods=['POST'])
def send_query():
    data = request.json
    if not data or "metadata" not in data:
        return jsonify({"error": "No metadata found"}), 400

    payload = {
        "vectors": [
            {
                "id": data.get("id"),
                "metadata": data.get("metadata"),
                "values": placeholder_vector
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Api-Key": PINECONE_API_KEY
    }

    try:
        response = requests.post(UPSERT_URL, json=payload, headers=headers)
        
        # Debugging
        print("Pinecone status code:", response.status_code)
        print("Pinecone response text:", response.text)

        response.raise_for_status()

        # Return metadata to frontend
        return jsonify({"results": [data.get("metadata")]})

    except requests.exceptions.RequestException as e:
        # Return full Pinecone response to frontend for debugging
        return jsonify({
            "error": str(e),
            "pinecone_status": response.status_code if 'response' in locals() else None,
            "pinecone_text": response.text if 'response' in locals() else None
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
