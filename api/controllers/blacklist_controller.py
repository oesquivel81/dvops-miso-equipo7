from flask import Blueprint, request, jsonify, g
from marshmallow import ValidationError
from application.dtos.request.blacklist_request_dto import BlacklistRequestDTO

from application.dtos.response.blacklist_response_dto import BlacklistResponseDTO
from application.services.blacklist_service import BlacklistService
from dependency_injector.wiring import inject, Provide
from infrastructure.container.dependency_container import DependencyContainer
from uuid import UUID
from flask import jsonify

blueprint = Blueprint("blacklist", __name__, url_prefix="/blacklists")

@blueprint.route("/", methods=["POST"])
@inject
def add_blacklist(blacklist_service: BlacklistService = Provide[DependencyContainer.blacklist_service]):
    schema = BlacklistRequestDTO()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    try:
        app_uuid = UUID(data["app_uuid"])
    except Exception:
        return jsonify({"errors": {"app_uuid": ["Invalid UUID"]}}), 400
    ip_address = request.remote_addr or "unknown"
    blacklist_service.add_to_blacklist(
        email=data["email"],
        app_uuid=app_uuid,
        blocked_reason=data.get("blocked_reason"),
        ip_address=ip_address
    )
    return jsonify({"message": "Email blacklisted"}), 201

@blueprint.route("/<string:email>", methods=["GET"])
@inject
def get_blacklist(email: str, blacklist_service: BlacklistService = Provide[DependencyContainer.blacklist_service]):
    result = blacklist_service.get_blacklist(email)
    if not result:
        return jsonify({"exists": False}), 404
    schema = BlacklistResponseDTO()
    return jsonify(schema.dump(result)), 200
