"""
This module contains all routes related to admin pages and related processes
"""

from flask import Blueprint, render_template, Response, make_response, \
    session, request, redirect, url_for
from sqlalchemy import and_
from app.ext.sqlalchemy.model import User, Privilege
from app.ext.sqlalchemy.database import db

# do not rename "blueprint" variable if you want to use auto import
blueprint: Blueprint = Blueprint(
    'admin',
    __name__,
    template_folder='templates'
)


@blueprint.route("/register", methods=["GET", "POST"])
def register_route() -> Response:
    """
    Secure page to register new users to the app.
    Requires admin privileges.
    """
    if "user_email" not in session:  # Logged in verification
        return redirect(url_for("auth.login_route"))

    admin_privilege = db.session.execute(
        db.select(User).join(Privilege).where(
            and_(
                User.email == session.get("user_email"),
                Privilege.privilege == "admin"
            )
        )).scalar()
    if admin_privilege is None:  # Admin verification
        return redirect(url_for("user.profile_route"))  # redirect to profile page as default

    form_errors = {
        "add_user_error": None,
        "edit_user_error": None
    }

    if request.method == "POST":
        if request.form.get("form_type") == "add_user":
            try:
                user = User()
                user.username = request.form.get("username")
                user.email = request.form.get("email")
                user.last_name = request.form.get("last_name")
                user.first_name = request.form.get("first_name")
                user.password = request.form.get("password")
                db.session.add(user)
                db.session.commit()
            except ValueError as e:
                db.session.rollback()
                form_errors["add_user_error"] = e.args[0]
        elif request.form.get("form_type") == "edit_user":
            # TODO
            pass

    users = db.session.execute(
        db.select(User)
    ).scalars().all()

    return make_response(render_template("admin/register.jinja2",
                                         users=users,
                                         **form_errors))
