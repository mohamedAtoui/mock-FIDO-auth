import json
import os
from pathlib import Path

USER_FILE = Path("users.json")

def _load_users():
    if USER_FILE.exists():
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def _save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

users = _load_users()

def init_users():
    # Only load once; do not overwrite
    global users
    users = _load_users()

def register_user(username, email, priv, pub):
    users[username] = {
        "email": email,
        "private_key": priv.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode(),
        "public_key": pub.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
    }
    _save_users(users)

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def get_user_keys(username):
    user = users[username]
    priv = serialization.load_pem_private_key(
        user["private_key"].encode(),
        password=None,
        backend=default_backend()
    )
    pub = serialization.load_pem_public_key(
        user["public_key"].encode(),
        backend=default_backend()
    )
    return {"private_key": priv, "public_key": pub}

def get_user_email(username):
    return users[username]["email"]

def user_exists(username):
    return username in users
