from flask import Blueprint, jsonify

blueprint = Blueprint("blacklist", __name__, url_prefix="/blacklists")

