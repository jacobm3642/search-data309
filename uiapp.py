from flask import Flask, render_template
from database_integration import Query, Database_handler

app = Flask(__name__)

@app.route('/')
def chat():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)
