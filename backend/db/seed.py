from datetime import date
from api.app import app
from db.base import db
from db.models.project import Project

PROJECTS = [
    Project(
        name="E-commerce Platform",
        description="Full-stack online store with product catalog, shopping cart, and Stripe checkout.",
        technologies=["Python", "Django", "PostgreSQL", "React", "Stripe"],
        start_date=date(2023, 1, 15),
        end_date=date(2023, 6, 30),
    ),
    Project(
        name="Real-time Chat App",
        description="Scalable WebSocket-based chat with rooms, direct messages, and read receipts.",
        technologies=["Node.js", "Socket.IO", "Redis", "MongoDB", "React"],
        start_date=date(2023, 3, 1),
        end_date=date(2023, 8, 15),
    ),
    Project(
        name="CI/CD Pipeline Tool",
        description="Self-hosted automation tool for building, testing, and deploying services.",
        technologies=["Go", "Docker", "Kubernetes", "gRPC", "PostgreSQL"],
        start_date=date(2023, 7, 1),
        end_date=None,
    ),
    Project(
        name="Data Visualization Dashboard",
        description="Interactive analytics dashboard with real-time charts and CSV export.",
        technologies=["Python", "FastAPI", "Pandas", "Vue.js", "D3.js"],
        start_date=date(2022, 9, 1),
        end_date=date(2023, 2, 28),
    ),
]


def seed() -> None:
    with app.app_context():
        existing = db.session.query(Project).count()
        if existing:
            print(f"Already has {existing} projects — skipping.")
            return
        db.session.add_all(PROJECTS)
        db.session.commit()
        print(f"Seeded {len(PROJECTS)} projects.")


if __name__ == "__main__":
    seed()