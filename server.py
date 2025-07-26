from flask import Flask, request, jsonify
import os, json

app = Flask(__name__)
DATA_FILE = 'account_data.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def home():
    return '✅ Server Match-2 Online'

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    if not username:
        return jsonify({'error': 'missing username'}), 400
    data = load_data()
    if username in data:
        return jsonify({'error': 'exists'}), 409
    data[username] = {'candy': 0, 'levels': [1]}
    save_data(data)
    return jsonify({'ok': True})

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    data = load_data()
    if username not in data:
        return jsonify({'error': 'not found'}), 404
    return jsonify({'ok': True, 'data': data[username]})

@app.route('/update', methods=['POST'])
def update():
    username = request.json.get('username')
    candy = request.json.get('candy')
    levels = request.json.get('levels')
    data = load_data()
    if username not in data:
        return jsonify({'error': 'not found'}), 404
    data[username] = {'candy': candy, 'levels': levels}
    save_data(data)
    return jsonify({'ok': True})

@app.route('/get/<username>', methods=['GET'])
def get_user_data(username):
    data = load_data()
    if username not in data:
        return jsonify({'error': 'not found'}), 404
    return jsonify({'ok': True, 'data': data[username]})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
