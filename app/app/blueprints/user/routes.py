from flask import (Blueprint, current_app, render_template, Response, make_response, session,
                   redirect, url_for, request)
from sqlalchemy.exc import SQLAlchemyError
from app.ext.sqlalchemy.model import User
from app.ext.sqlalchemy.database import db


# do not rename "blueprint" variable if you want to use auto import
blueprint: Blueprint = Blueprint(
    'user',
    __name__,
    template_folder='templates'
)


@blueprint.route("/profile", methods=["GET", "POST"])
def profile_route() -> Response:
    """
    Secure page to view user details. It allows to update username, password and personal info.
    :return: Response
    """

    if "user_email" not in session:  # Logged in verification
        return redirect(url_for("auth.login_route"))

    # Get session user data from database
    user = db.session.execute(
        db.select(User).
        where(
            User.email == session.get("user_email")
        )).scalar()

    # Form errors for jinja2 template
    form_errors = {
        "username_error": None,
        "password_error": None,
        "personal_info_error": None
    }

    if request.method == "POST":
        """
        Update user data in database based on form_type
        """
        if request.form.get("form_type") == "update_username":
            try:
                user.username = request.form.get("username")
                user.verified = True  # tell the db that there are changes to commit
                db.session.commit()
            except ValueError as e:
                db.session.rollback()  # cancel changes
                form_errors["username_error"] = e.args[0]

        elif request.form.get("form_type") == "update_password":
            is_valid_password = user.check_password(request.form.get("password"))
            is_confirmed_password = request.form.get("new_password") == request.form.get("confirm_password")
            if is_valid_password and is_confirmed_password:
                try:
                    user.password = request.form.get("confirm_password")
                    user.verified = True  # tell the db that there are changes to commit
                    db.session.commit()
                except ValueError as e:
                    db.session.rollback()  # cancel changes
                    form_errors["password_error"] = e.args[0]
            elif not is_valid_password:
                form_errors["password_error"] = ("Invalid password",)
            elif not is_confirmed_password:
                form_errors["password_error"] = ("Password confirmation does not match",)

        elif request.form.get("form_type") == "update_personal_info":
            try:
                user.first_name = request.form.get("first_name")
                user.last_name = request.form.get("last_name")
                user.profile_description = request.form.get("profile_description")
                user.verified = True  # tell the db that there are changes to commit
                db.session.commit()
            except ValueError as e:
                db.session.rollback()  # cancel changes
                form_errors["personal_info_error"] = e.args[0]

    return make_response(render_template("profile/profile.jinja2", user=user, **form_errors))
