from flask import jsonify
from flask_smorest import Blueprint

from db.base import db

blp = Blueprint("health", __name__, description="Service health check")

@blp.get("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = str(e)
    return jsonify({"status": "ok", "db": db_status})
