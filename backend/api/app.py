from flask import Flask
from flask_smorest import Api

from api.health import blp as health
from api.projects import blp as projects_blp
from config import Config
from db import models as _models  # noqa: F401 — registers models with SQLAlchemy
from db.base import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("DATABASE_URL environment variable is required")

    if not app.config.get("API_KEY"):
        app.logger.warning("API_KEY is not set — all requests will return 401")

    db.init_app(app)

    api = Api(app)
    api.register_blueprint(health, url_prefix="/api")
    api.register_blueprint(projects_blp, url_prefix="/api")

    return app


app = create_app()
