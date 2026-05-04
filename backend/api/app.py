import os

from flask import Flask
from flask_smorest import Api

from db.base import db
from db import models as _models  # noqa: F401 — registers models with SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///portfolio.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["API_TITLE"] = "Project Portfolio API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["API_SPEC_OPTIONS"] = {
        "components": {
            "securitySchemes": {"BearerAuth": {"type": "http", "scheme": "bearer"}}
        },
        "security": [{"BearerAuth": []}],
    }

    db.init_app(app)

    api = Api(app)

    from api.projects import blp as projects_blp
    from api.health import blp as health

    api.register_blueprint(health, url_prefix="/api")
    api.register_blueprint(projects_blp, url_prefix="/api")

    return app


app = create_app()
