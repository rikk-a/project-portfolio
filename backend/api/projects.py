import os

import sqlalchemy as sa
from flask import request
from sqlalchemy.dialects.postgresql import JSONB
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from api.schemas import ProjectPageSchema, ProjectQuerySchema, ProjectSchema
from db.base import db
from db.models.project import Project

blp = Blueprint("projects", __name__, description="CRUD operations for projects")


@blp.before_request
def check_auth():
    api_key = os.environ.get("API_KEY")
    if api_key and request.headers.get("Authorization") != f"Bearer {api_key}":
        abort(401, message="Unauthorized")


@blp.route("/projects")
class ProjectList(MethodView):
    @blp.arguments(ProjectQuerySchema, location="query")
    @blp.response(200, ProjectPageSchema)
    def get(self, args):
        """List projects with filtering, sorting, search and pagination"""
        stmt = sa.select(Project)

        if args["search"]:
            stmt = stmt.where(
                sa.or_(
                    Project.name.ilike(f"%{args['search']}%"),
                    Project.description.ilike(f"%{args['search']}%"),
                )
            )

        if args["technology"]:
            stmt = stmt.where(
                sa.or_(
                    *[Project.technologies.contains(sa.cast([t], JSONB)) for t in args["technology"]]
                )
            )

        col = getattr(Project, args["sort_by"])
        stmt = stmt.order_by(col.desc() if args["order"] == "desc" else col.asc())

        pagination = db.paginate(
            stmt, page=args["page"], per_page=args["per_page"], error_out=False
        )

        return {
            "data": pagination.items,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
        }

    @blp.arguments(ProjectSchema)
    @blp.response(201, ProjectSchema)
    def post(self, data):
        """Create a new project"""
        project = Project(**data)
        db.session.add(project)
        db.session.commit()
        return project


@blp.route("/projects/<int:project_id>")
class ProjectDetail(MethodView):
    @blp.response(200, ProjectSchema)
    def get(self, project_id):
        """Get a single project by ID"""
        return db.get_or_404(Project, project_id)

    @blp.response(204)
    def delete(self, project_id):
        """Delete a project"""
        project = db.get_or_404(Project, project_id)
        db.session.delete(project)
        db.session.commit()