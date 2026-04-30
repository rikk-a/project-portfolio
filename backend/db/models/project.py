import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from db.base import db


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(sa.Integer, primary_key=True)
    name = db.Column(sa.String(255), nullable=False)
    description = db.Column(sa.Text)
    technologies = db.Column(JSONB)
    start_date = db.Column(sa.Date, nullable=False)
    end_date = db.Column(sa.Date)