import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Auth
    API_KEY = os.environ.get("API_KEY", "")

    # OpenAPI / Swagger
    API_TITLE = "Project Portfolio API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    API_SPEC_OPTIONS = {
        "components": {
            "securitySchemes": {"BearerAuth": {"type": "http", "scheme": "bearer"}}
        },
        "security": [{"BearerAuth": []}],
    }


class TestingConfig(Config):
    TESTING = True
    API_KEY = os.environ.get("TEST_API_KEY", "test-api-key")