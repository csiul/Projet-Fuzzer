from flask import Blueprint, make_response, render_template, current_app, Response
from sqlalchemy import text
from app.ext.sqlalchemy.database import db


blueprint: Blueprint = Blueprint(
    'index',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@blueprint.route("/", methods=["get"])
def index_route() -> Response:

    result = db.session.execute(text("SELECT 1"))
    value = result.scalar()
    return make_response(
        render_template(
            "index.jinja2",
            sql_value=value
        )
    )
