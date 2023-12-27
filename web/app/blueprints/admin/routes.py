"""
This module contains all routes related to admin pages and related processes
"""
from flask import Blueprint, render_template, Response, make_response, request
from sqlalchemy.exc import IntegrityError
from app.ext.sqlalchemy.model import User
from app.ext.sqlalchemy.database import db
from app.blueprints.auth.routes import privileges_required_factory

# do not rename "blueprint" variable if you want to use auto import
blueprint: Blueprint = Blueprint(
    'admin',
    __name__,
    template_folder='templates'
)


@blueprint.route("/register", methods=["GET", "POST"])
@privileges_required_factory(("admin",))  # admin privileges required
def register_route() -> Response:
    """
    Secure page to register new users to the app.
    Requires admin privileges.
    """
    form_errors = {
        "add_user_error": None,
    }

    if request.method == "POST":
        if request.form.get("form_type") == "add_user":
            try:
                user = User(
                    username=request.form.get("username"),
                    email=request.form.get("email") if request.form.get("email") != "" else None,
                    last_name=request.form.get("last_name"),
                    first_name=request.form.get("first_name"),
                    password=request.form.get("password"))
                db.session.add(user)
                db.session.commit()
            except ValueError as e:
                db.session.rollback()
                form_errors["add_user_error"] = e.args[0]
            except IntegrityError:
                db.session.rollback()
                form_errors["add_user_error"] = ("Le nom d'utilisateur ou le courriel est déjà pris",)

    return make_response(render_template("admin/register.jinja2",
                                         **form_errors))


@blueprint.route("/manage", methods=["GET", "POST"])
@privileges_required_factory(("admin",))  # admin privileges required
def manage_route() -> Response:
    """
    Secure page to modify existing users of the app.
    Requires admin privileges.
    """
    form_errors={
        "update_user_error": None,
        "delete_user_error": None,
    }
    users = db.session.execute(
        db.select(User)
    ).scalars().all()

    return make_response(render_template("admin/manage.jinja2",
                                         **form_errors,
                                         users=users))
