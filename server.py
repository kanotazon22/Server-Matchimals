from flask import Flask, request, jsonify
import os, json
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'account_data.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def timestamp():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def home():
    print(f"{timestamp()} ⏺️ / called")
    return '✅ Server Match-2 Online'

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    print(f"{timestamp()} 📥 /register -> {username}")
    if not username:
        return jsonify({'error': 'missing username'}), 400
    data = load_data()
    if username in data:
        print(f"{timestamp()} ❌ Register failed: already exists")
        return jsonify({'error': 'exists'}), 409
    data[username] = {'candy': 0, 'levels': [1]}
    save_data(data)
    print(f"{timestamp()} ✅ Register OK for {username}")
    return jsonify({'ok': True})

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    print(f"{timestamp()} 🔑 /login -> {username}")
    data = load_data()
    if username not in data:
        print(f"{timestamp()} ❌ Login failed: {username} not found")
        return jsonify({'error': 'not found'}), 404
    print(f"{timestamp()} ✅ Login OK for {username}")
    return jsonify({'ok': True, 'data': data[username]})

@app.route('/update', methods=['POST'])
def update():
    username = request.json.get('username')
    candy = request.json.get('candy')
    levels = request.json.get('levels')
    print(f"{timestamp()} 📤 /update -> {username} | candy: {candy} | levels: {levels}")
    data = load_data()
    if username not in data:
        print(f"{timestamp()} ❌ Update failed: {username} not found")
        return jsonify({'error': 'not found'}), 404
    data[username] = {'candy': candy, 'levels': levels}
    save_data(data)
    print(f"{timestamp()} ✅ Update OK for {username}")
    return jsonify({'ok': True})

@app.route('/dump', methods=['GET'])
def dump_data():
    data = load_data()
    print(f"{timestamp()} 📂 /dump requested")
    return jsonify(data)

if __name__ == '__main__':
    print(f"{timestamp()} 🚀 Server starting on 0.0.0.0:5000")
    app.run(host='0.0.0.0')
