from flask import request, jsonify
from functools import wraps
from infrastructure.config.settings import Settings

def auth_middleware():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401
    token = auth_header.split(" ", 1)[1]
    if token != Settings.BEARER_TOKEN:
        return jsonify({"error": "Invalid token"}), 401
