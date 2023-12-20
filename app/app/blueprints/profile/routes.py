from flask import (Blueprint, current_app, render_template, Response, make_response, session,
                   redirect, url_for, request)
from sqlalchemy.exc import SQLAlchemyError
from app.ext.sqlalchemy.model import User
from app.ext.sqlalchemy.database import db


# do not rename "blueprint" variable if you want to use auto import
blueprint: Blueprint = Blueprint(
    'profile',
    __name__,
    template_folder='templates'
)


@blueprint.route("/profile", methods=["GET", "POST"])
def profile_route() -> Response:
    """
    Secure page to view user profile details. It allows to update username, password and personal info.
    :return: Response
    """

    if "user_email" not in session:  # Logged in verification
        return redirect(url_for("login.login_route"))

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
            user.username = request.form.get("username")
            user.verified = True  # tell the db that there are changes to commit
            try:
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()  # cancel changes
                form_errors["username_error"] = e

        elif request.form.get("form_type") == "update_password":
            is_valid_password = user.check_password(request.form.get("password"))
            is_confirmed_password = request.form.get("new_password") == request.form.get("confirm_password")
            is_strong_password, password_criteria = User.check_password_strength(request.form.get("confirm_password"))
            if is_valid_password and is_confirmed_password and is_strong_password:
                user.set_password(request.form.get("confirm_password"))
                user.verified = True  # tell the db that there are changes to commit
                try:
                    db.session.commit()
                except SQLAlchemyError as e:
                    db.session.rollback()  # cancel changes
                    form_errors["password_error"] = e
            else:
                if not is_valid_password:
                    form_errors["password_error"] = "Mot de passe invalide"
                elif not is_confirmed_password:
                    form_errors["password_error"] = "Le nouveau mot de passe et la confirmation ne correspondent pas"
                elif not is_strong_password:
                    form_errors["password_error"] = "Votre mot de passe n'est pas assez fort"

        elif request.form.get("form_type") == "update_personal_info":
            user.first_name = request.form.get("first_name")
            user.last_name = request.form.get("last_name")
            user.profile_description = request.form.get("profile_description")
            user.verified = True  # tell the db that there are changes to commit
            try:
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()  # cancel changes
                form_errors["personal_info_error"] = e

    return make_response(render_template("profile.jinja2", user=user, **form_errors))
