import sqlalchemy as sa
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB

from db.base import db


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(sa.Integer, primary_key=True)
    name = db.Column(sa.String(255), nullable=False)
    description = db.Column(sa.Text)
    technologies = db.Column(JSONB) #This field is jsonb for search purposes, but I would create a separate table
    start_date = db.Column(sa.Date, nullable=False)
    end_date = db.Column(sa.Date)

    __table_args__ = (
        Index("ix_projects_technologies_gin", "technologies", postgresql_using="gin"),
    )
