import pytest
from datetime import date

from api.app import create_app
from db.base import db as _db
from db.models.project import Project


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        _db.create_all()
        yield app
        _db.engine.dispose()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):
    yield
    _db.session.rollback()
    for table in reversed(_db.metadata.sorted_tables):
        _db.session.execute(table.delete())
    _db.session.commit()


@pytest.fixture()
def sample_project(app):
    project = Project(
        name="Test Project",
        description="A test project description",
        technologies=["Python", "Flask"],
        start_date=date(2024, 1, 1),
        end_date=None,
    )
    _db.session.add(project)
    _db.session.commit()
    _db.session.refresh(project)
    return project
