from app import create_app, db
from flask import Flask, Blueprint
application = create_app()
health_bp = Blueprint("health", __name__)

@health_bp.route("/", methods=["GET"])
def index():
    return {"message": "API running"}, 200
if __name__ == '__main__':
     with application.app_context():
        db.create_all()  # Crea la base de datos si no existe
        application.run(host="0.0.0.0", port=5000) 