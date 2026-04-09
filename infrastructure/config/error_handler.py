import logging
from flask import jsonify, request
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

logger = logging.getLogger("blacklist")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_marshmallow_error(e):
        logger.warning(f"Validation error: {e.messages} | Path: {request.path}")
        return jsonify({"errors": e.messages}), 400

    @app.errorhandler(404)
    def not_found(e):
        logger.info(f"404 Not Found: {request.path}")
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(401)
    def unauthorized(e):
        logger.warning(f"401 Unauthorized: {request.path}")
        return jsonify({"error": "Unauthorized"}), 401

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        logger.error(f"HTTPException: {e.code} {e.name} - {e.description} | Path: {request.path}")
        response = e.get_response()
        response.data = jsonify({
            "error": e.name,
            "description": e.description
        }).data
        response.content_type = "application/json"
        return response, e.code

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception(f"Unhandled Exception: {str(e)} | Path: {request.path}")
        return jsonify({"error": "Internal Server Error"}), 500
