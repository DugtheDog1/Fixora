from flask import Flask, render_template, request, jsonify
from utils.ai import generate_reply
from utils.categorize import categorize_issue
import json
import os

app = Flask(__name__)

DATA_FILE = 'data/requests.json'

def load_requests():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []

def save_request(data):
    requests = load_requests()
    requests.append(data)
    with open(DATA_FILE, 'w') as f:
        json.dump(requests, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html', requests=load_requests())

@app.route('/submit', methods=['POST'])
def submit():
    issue_text = request.form['description']
    category = categorize_issue(issue_text)
    reply = generate_reply(issue_text, category)

    new_request = {
        "description": issue_text,
        "category": category,
        "status": "Open",
        "reply": reply
    }

    save_request(new_request)
    return jsonify(new_request)

if __name__ == '__main__':
    app.run(debug=True)
