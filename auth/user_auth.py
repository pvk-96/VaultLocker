# This is the Authorization code
import json
import os
import bcrypt

USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'users.json')


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users[username] = hashed.decode()
    save_users(users)
    return True, "Registration successful."

def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found."
    hashed = users[username].encode()
    if bcrypt.checkpw(password.encode(), hashed):
        return True, "Login successful."
    else:
        return False, "Incorrect password."

def update_user_password(username, new_password):
    users = load_users()
    if username not in users:
        return False
    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    users[username] = hashed.decode()
    save_users(users)
    return True 
