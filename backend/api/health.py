from flask import jsonify
from flask_smorest import Blueprint

from db.base import db

blp = Blueprint("health", __name__, description="Service health check")

@blp.get("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"
    healthy = db_status == "ok"
    return jsonify({"status": "ok" if healthy else "error", "db": db_status}), (200 if healthy else 503)
