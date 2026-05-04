import marshmallow as ma


class ProjectSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.Str(required=True, validate=ma.validate.Length(min=3, max=255))
    description = ma.fields.Str(allow_none=True)
    technologies = ma.fields.List(ma.fields.Str(), load_default=None, allow_none=True)
    start_date = ma.fields.Date(required=True)
    end_date = ma.fields.Date(load_default=None, allow_none=True)

    @ma.validates_schema
    def validate_dates(self, data, **kwargs):
        start = data.get("start_date")
        end = data.get("end_date")
        if start and end and end <= start:
            raise ma.ValidationError("end_date must be after start_date", "end_date")


class ProjectQuerySchema(ma.Schema):
    page = ma.fields.Int(load_default=1, validate=ma.validate.Range(min=1))
    per_page = ma.fields.Int(load_default=10, validate=ma.validate.Range(min=1, max=100))
    search = ma.fields.Str(load_default="")
    technology = ma.fields.List(ma.fields.Str(), load_default=[])
    sort_by = ma.fields.Str(
        load_default="id",
        validate=ma.validate.OneOf(["id", "name", "start_date", "end_date"]),
    )
    order = ma.fields.Str(
        load_default="asc",
        validate=ma.validate.OneOf(["asc", "desc"]),
    )


class ProjectPageSchema(ma.Schema):
    data = ma.fields.List(ma.fields.Nested(ProjectSchema))
    page = ma.fields.Int()
    per_page = ma.fields.Int()
    total = ma.fields.Int()
    pages = ma.fields.Int()
