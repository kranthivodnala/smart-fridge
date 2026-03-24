from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

items = []

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    item = {
        "name": data["name"],
        "expiry": data["expiry"]
    }
    items.append(item)
    return jsonify({"message": "Item added"}), 201

@app.route('/items/<name>', methods=['DELETE'])
def delete_item(name):
    global items
    items = [item for item in items if item["name"] != name]
    return jsonify({"message": "Item deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)