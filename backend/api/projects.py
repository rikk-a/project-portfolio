import sqlalchemy as sa
from flask import current_app, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.dialects.postgresql import JSONB

from api.schemas import ProjectPageSchema, ProjectQuerySchema, ProjectSchema
from db.base import db
from db.models.project import Project
from db.session import session_scope

blp = Blueprint("projects", __name__, description="CRUD operations for projects")

_SORT_COLUMNS = {
    "id": Project.id,
    "name": Project.name,
    "start_date": Project.start_date,
    "end_date": Project.end_date,
}


# If that is internal service than token auth is ok, but It would probably
# be used user/password auth with JWT in prod
@blp.before_request
def check_auth():
    api_key = current_app.config.get("API_KEY")
    if not api_key or request.headers.get("Authorization") != f"Bearer {api_key}":
        abort(401, message="Unauthorized")


def _escape_like(value: str) -> str:
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


@blp.route("/projects")
class ProjectList(MethodView):
    @blp.arguments(ProjectQuerySchema, location="query")
    @blp.response(200, ProjectPageSchema)
    def get(self, args):
        """List projects with filtering, sorting, search and pagination"""
        stmt = sa.select(Project)

        if args["search"]:
            escaped = _escape_like(args["search"])
            stmt = stmt.where(
                sa.or_(
                    Project.name.ilike(f"%{escaped}%", escape="\\"),
                    Project.description.ilike(f"%{escaped}%", escape="\\"),
                )
            )

        if args["technology"]:
            stmt = stmt.where(
                sa.or_(
                    *[Project.technologies.contains(sa.cast([t], JSONB)) for t in args["technology"]]
                )
            )

        col = _SORT_COLUMNS[args["sort_by"]]
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
        with session_scope() as session:
            project = Project(**data)
            session.add(project)
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
        with session_scope() as session:
            project = db.get_or_404(Project, project_id)
            session.delete(project)
