from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# User data file
USER_FILE = 'users.txt'

# Ensure the file exists
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w') as f:
        pass


def load_users():
    with open(USER_FILE, 'r') as f:
        return [eval(line.strip()) for line in f.readlines()]

def save_users(users):
    with open(USER_FILE, 'w') as f:
        for user in users:
            f.write(f"{user}\n")

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    if not data.get('email') or not data.get('age'):
        return jsonify({"error": "Email and age are required"}), 400

    users = load_users()
    if any(u['email'] == data['email'] for u in users):
        return jsonify({"error": "User already exists"}), 400

    users.append(data)
    save_users(users)
    return jsonify({"message": "User added successfully"}), 201

@app.route('/users/<email>', methods=['GET'])
def get_user(email):
    users = load_users()
    user = next((u for u in users if u['email'] == email), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.route('/users/<email>', methods=['PUT'])
def update_user(email):
    data = request.json
    users = load_users()
    user = next((u for u in users if u['email'] == email), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.update(data)
    save_users(users)
    return jsonify({"message": "User updated successfully"})

@app.route('/users/<email>', methods=['DELETE'])
def delete_user(email):
    users = load_users()
    users = [u for u in users if u['email'] != email]
    save_users(users)
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == '__main__':
    app.run(port=5000)
