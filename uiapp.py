from flask import Flask, render_template, request, jsonify
from database_integration import Database_handler, Query

app = Flask(__name__)

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

    q = Query().set_body(query_text).set_count(10)

    try:
        results = db_handler.search(q)

        # change the format when we decided what structure
        formatted_results = []
        for r in results.items:
            formatted_results.append({
                "title": getattr(r, "title", "Untitled"),
                "snippet": getattr(r, "snippet", str(r))
            })

        return jsonify({"results": formatted_results})

    except Exception as e:
        print("Error during search:", e)
        return jsonify({"error": "Search failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)
