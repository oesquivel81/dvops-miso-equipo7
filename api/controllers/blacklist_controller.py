from flask import Blueprint, jsonify

blueprint = Blueprint("blacklist", __name__, url_prefix="/blacklists")

@blueprint.route("/dummy", methods=["GET"])
def dummy_blacklist():
    return jsonify({
        "status": "ok",
        "data": [
            {"email": "test@example.com", "blacklisted": True},
            {"email": "foo@bar.com", "blacklisted": False}
        ]
    })

@blueprint.route("/<string:email>", methods=["GET"])
@inject
def get_blacklist(email: str, blacklist_service: BlacklistService = Provide[DependencyContainer.blacklist_service]):
    result = blacklist_service.get_blacklist(email)
    if not result:
        return jsonify({"exists": False}), 404
    schema = BlacklistResponseDTO()
    return jsonify(schema.dump(result)), 200
