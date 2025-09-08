from flask import Flask, render_template, request, jsonify
from database_integration import Database_handler, Query
import random

app = Flask(__name__)

USE_MOCK = True   # <<< flip this False when DB is ready
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
                "abstract": f"This is a mock abstract for paper {i+1}. It demonstrates how semantic search works.",
                "keyword": "AI, Machine Learning, NLP",
                "category": random.choice(["cs.CL", "cs.LG", "stat.ML"]),
                "date_published": random.choice(
                    ["2019-06-01", "2020-07-15", "2021-09-30", "2022-12-10", "2023-04-22"]
                ),
                "arxiv_url": f"https://arxiv.org/abs/1234.{1000+i}",
                "pdf_url": f"https://arxiv.org/pdf/1234.{1000+i}.pdf",
                "similarity": round(random.uniform(0.7, 0.99), 3)
            })
        return jsonify({"results": mock_results})

    # ---- Real DB search ----
    q = Query().from_dict(data)
    try:
        results = db_handler.search(q)
        formatted_results = []

        for r in getattr(results, "items", []):
            metadata = getattr(r, "metadata", {})

            formatted_results.append({
                "title": metadata.get("title", "Untitled"),
                "abstract": metadata.get("abstract", "No abstract available"),
                "keyword": metadata.get("keyword", "N/A"),
                "category": metadata.get("category", "N/A"),
                "date_published": metadata.get("date_published", "N/A"),
                "arxiv_url": metadata.get("arxiv_url", "#"),
                "pdf_url": metadata.get("pdf_url", "#"),
                "similarity": getattr(r, "similarity", None)
            })

        return jsonify({"results": formatted_results})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
