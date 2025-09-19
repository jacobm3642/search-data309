from flask import Flask, render_template, request, jsonify
from database_integration import Database_handler
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# Load embedding model once at startup
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def embed(text):
    """Generate embedding for a query string"""
    return model.encode(text).tolist()

db_handler = Database_handler()

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    if not data or "query" not in data:
        return jsonify({"error": "No query provided"}), 400

    query_text = data["query"]
    topk = int(data.get("topk", 10))

    try:
        # Generate embedding
        vector = embed(query_text)

        # Ensure DB is connected
        db_handler.connect_db()

        # Query Pinecone
        results = db_handler.index_target.query(
            vector=vector,
            top_k=topk,
            include_metadata=True
        )

        formatted_results = []
        for r in getattr(results, "matches", []):
            metadata = getattr(r, "metadata", {})
            formatted_results.append({
                "title": metadata.get("title", "Untitled"),
                "date_published": metadata.get("date_published", "N/A"),
                "abstract": metadata.get("abstract", "No abstract available"),
                "similarity": getattr(r, "score", None),
                "arxiv_url": metadata.get("arxiv_url", "#"),
                "pdf_url": metadata.get("pdf_url", "#"),
                "category": metadata.get("category", "N/A"),
                "keyword": metadata.get("keyword", "N/A"),
            })

        return jsonify({"results": formatted_results})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
