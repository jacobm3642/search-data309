from flask import Flask, render_template, request, jsonify
from database_integration import Database_handler, Query
import random

app = Flask(__name__)
USE_MOCK = True #change to false when don need the mock data

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

    if USE_MOCK:
        # ---- Mock results ----
        mock_results = []
        for i in range(topk):
            mock_results.append({
                "title": f"Sample Paper {i+1}",
                "author": f"Author {chr(65+i%26)}",
                "year": random.choice([2018, 2019, 2020, 2021, 2022, 2023]),
                "abstract": f"This is a mock abstract for paper {i+1}. It describes how semantic search improves research.",
                "similarity": round(random.uniform(0.7, 0.99), 3)
            })
        return jsonify({"results": mock_results})

    # ---- Real DB search ----
    q = Query().set_body(query_text).set_count(topk)
    try:
        results = db_handler.search(q)
        formatted_results = []
        for r in getattr(results, "items", []):
            formatted_results.append({
                "title": getattr(r, "title", "Untitled"),
                "author": getattr(r, "author", "Unknown author"),
                "year": getattr(r, "year", "N/A"),
                "abstract": getattr(r, "abstract", getattr(r, "snippet", "No abstract available")),
                "similarity": getattr(r, "similarity", None)
            })

        return jsonify({"results": formatted_results})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
