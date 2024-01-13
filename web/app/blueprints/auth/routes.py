"""
This module contains all routes related to authentication processes and their logic
"""
from functools import wraps
from flask import Blueprint, render_template, session, request, redirect, url_for, Response, make_response
from app.ext.sqlalchemy.model import User
from app.ext.sqlalchemy.database import db

# do not rename "blueprint" variable if you want to use auto import
blueprint: Blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)


def user_in_session() -> bool:
    """
    Checks if user is logged in
    :return: True if user is logged in, False otherwise
    """
    return "user_uid" in session


def privileges_required_factory(privileges_required: tuple):
    """
    Factory to create a route decorator to check if user is logged in and or if it has certain privileges
    before accessing a route.
    :param privileges_required: tuple of privileges to check.
        Supply an empty tuple to only check if user is logged in.
    :return: route decorator
    """
    def decorator(f):
        """
        Decorator to check if user is logged in and or if it has certain privileges
        :param f: function to decorate
        :return: decorated function
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not user_in_session():  # Logged in verification
                return redirect(url_for("auth.login_route"))
            user = db.session.execute(
                db.select(User).where(
                    (User.uid == session.get("user_uid"))
                )).scalar()
            user_privileges = {privilege.privilege for privilege in user.privileges}
            if not set(privileges_required).issubset(user_privileges):  # Privilege verification
                return redirect(url_for("user.profile_route"))  # redirect to profile page as default
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@blueprint.route("/login", methods=["GET", "POST"])
def login_route() -> Response:
    """
    Unsecure page to log in. If user is already logged in, redirect to profile page.
    :return: Response
    """
    # If user is already logged in, redirect to profile page. Otherwise, show login page.
    if user_in_session():
        return redirect(url_for("user.profile_route"))

    login_error = None

    if request.method == "POST":
        # Get user from database and check if password is valid.
        user = db.session.execute(
            db.select(User).
            where(
                User.username == request.form.get("username")
            )).scalar_one_or_none()
        is_valid_password = user.check_password(request.form.get("password")) if user is not None else False
        if is_valid_password:
            session["user_uid"] = user.uid
            return redirect(url_for("user.profile_route"))
        login_error = "Nom d'utilisateur ou mot de passe invalide"

    return make_response(render_template("login/login.jinja2", error=login_error))


@blueprint.route("/logout", methods=["GET"])
def logout_route() -> Response:
    """
    Deletes session data and redirects to login page
    """
    session.clear()
    return redirect(url_for(".login_route"))
