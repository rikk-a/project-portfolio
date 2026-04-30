def test_create_project_returns_201(client):
    payload = {
        "name": "New Project",
        "description": "Created in test",
        "technologies": ["Python", "Docker"],
        "start_date": "2024-03-01",
    }
    response = client.post("/api/projects", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] is not None
    assert data["name"] == payload["name"]
    assert data["technologies"] == payload["technologies"]


def test_delete_project_returns_204(client, sample_project):
    response = client.delete(f"/api/projects/{sample_project.id}")
    assert response.status_code == 204

    response = client.get(f"/api/projects/{sample_project.id}")
    assert response.status_code == 404


def test_filter_by_technology_returns_matching_projects(client, app):
    from db.base import db
    from db.models.project import Project
    from datetime import date

    with app.app_context():
        db.session.add_all([
            Project(name="Flask App", technologies=["Python", "Flask"], start_date=date(2024, 1, 1)),
            Project(name="Go Service", technologies=["Go", "Docker"], start_date=date(2024, 2, 1)),
        ])
        db.session.commit()

    response = client.get("/api/projects?technology=Python")

    assert response.status_code == 200
    data = response.get_json()
    assert all("Python" in p["technologies"] for p in data["data"])
    assert not any(p["name"] == "Go Service" for p in data["data"])


def test_list_projects_returns_200_and_list(client, sample_project):
    response = client.get("/api/projects")

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data["data"], list)
    assert len(data["data"]) >= 1


def test_get_project_returns_correct_object(client, sample_project):
    response = client.get(f"/api/projects/{sample_project.id}")

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == sample_project.id
    assert data["name"] == sample_project.name
    assert data["technologies"] == sample_project.technologies


def test_get_nonexistent_project_returns_404(client):
    response = client.get("/api/projects/999")

    assert response.status_code == 404