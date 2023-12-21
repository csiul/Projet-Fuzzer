from flask import Blueprint, current_app, render_template, session, request, redirect, url_for, Response, make_response
from sqlalchemy import and_
from app.ext.sqlalchemy.model import User
from app.ext.sqlalchemy.database import db

# do not rename "blueprint" variable if you want to use auto import
blueprint: Blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)


@blueprint.route("/login", methods=["GET", "POST"])
def login_route() -> Response:
    """
    Unsecure page to log in. If user is already logged in, redirect to profile page.
    :return: Response
    """
    if request.method == "POST":
        """
        Get user from database and check if password is valid.
        """
        user = db.session.execute(
            db.select(User).
            where(
                User.email == request.form.get("email")
            )).scalar_one_or_none()
        is_valid_password = user.check_password(request.form.get("password")) if user is not None else False
        if is_valid_password:
            session["user_email"] = user.email
            return redirect(url_for("user.profile_route"))
        else:
            return redirect(url_for(".login_route"))

    if request.method == "GET":
        """
        If user is already logged in, redirect to profile page. Otherwise, show login page.
        """
        if "user_email" in session:
            return redirect(url_for("user.profile_route"))
        else:
            return make_response(render_template("login/login.jinja2"))


@blueprint.route("/logout", methods=["GET"])
def logout_route() -> Response:
    session.clear()
    return redirect(url_for(".login_route"))