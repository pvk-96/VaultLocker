import os
import json
from datetime import datetime

VAULT_DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'vault_data.json')


def load_vault():
    if not os.path.exists(VAULT_DATA_FILE):
        return []
    with open(VAULT_DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_vault(entries):
    with open(VAULT_DATA_FILE, 'w') as f:
        json.dump(entries, f, indent=2)

def add_file_entry(original_name, stored_name, username, status="encrypted"):
    entries = load_vault()
    entry = {
        "original_name": original_name,
        "stored_name": stored_name,
        "username": username,
        "date": datetime.now().isoformat(timespec='seconds'),
        "status": status
    }
    entries.append(entry)
    save_vault(entries)
    return entry

def list_file_entries(username):
    return [e for e in load_vault() if e.get("username") == username]

def delete_file_entry(stored_name, username):
    entries = load_vault()
    entries = [e for e in entries if not (e["stored_name"] == stored_name and e.get("username") == username)]
    save_vault(entries) 