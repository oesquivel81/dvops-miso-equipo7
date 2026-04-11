from flask import Flask, Blueprint, jsonify, request
from application.services.blacklist_service import BlacklistService

# Crear la app
app = Flask(__name__)

# Instanciar el servicio dummy
blacklist_service = BlacklistService()

# Definir blueprint dummy
dummy_blueprint = Blueprint("blacklist", __name__, url_prefix="/blacklists")


# Endpoint GET para obtener toda la blacklist dummy
@dummy_blueprint.route("/", methods=["GET"])
def get_all_blacklist():
    # Devuelve todos los datos dummy usando el método del repositorio
    return jsonify({
        "status": "ok",
        "data": blacklist_service.repository.get_all()
    })

@dummy_blueprint.route("/<string:email>", methods=["GET"])
def get_blacklist(email):
    result = blacklist_service.get_blacklist(email)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({"exists": False}), 404

# Endpoint POST dummy para agregar un email a la blacklist
@dummy_blueprint.route("/", methods=["POST"])
def add_blacklist():
    data = request.get_json()
    email = data.get("email")
    blacklisted = data.get("blacklisted", True)
    if not email:
        return jsonify({"error": "email is required"}), 400
    blacklist_service.add_to_blacklist(email, blacklisted)
    return jsonify({"message": "Email added to blacklist", "email": email, "blacklisted": blacklisted}), 201

# Registrar blueprint
app.register_blueprint(dummy_blueprint)

# Endpoint health
@app.route("/health")
def health():
    return "healthy", 200
