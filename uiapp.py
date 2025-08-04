from flask import Flask, render_template, request

app = Flask(__name__)

data = [
    "How to learn Python",
    "Flask web development",
    "Semantic Search Engine project",
    "Diabetes prediction using machine learning",
    "Introduction to Data Science"
]

@app.route('/')
def search_page():
    return render_template('search.html')

@app.route('/results', methods=['POST'])
def search_results():
    query = request.form['query'].lower()
    matches = [item for item in data if query in item.lower()]
    return render_template('results.html', query=query, results=matches)

if __name__ == '__main__':
    app.run(debug=True)
