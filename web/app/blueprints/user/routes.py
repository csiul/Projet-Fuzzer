"""
This module contains all routes related to user pages and related processes
"""

from flask import Blueprint, render_template, Response, make_response, session, request, jsonify
from sqlalchemy.exc import IntegrityError

from app.ext.sqlalchemy.model import User
from app.ext.sqlalchemy.database import db
from app.blueprints.auth.routes import privileges_required_factory


# do not rename "blueprint" variable if you want to use auto import
blueprint: Blueprint = Blueprint(
    'user',
    __name__,
    template_folder='templates'
)


@blueprint.route("/profile", methods=["GET"])
@privileges_required_factory(tuple())  # no privileges required, just logged in
def profile_route() -> Response:
    """
    Secure page to view user details. It allows to update username, password and personal info.
    :return: Response
    """
    # Get session user data from database
    user = db.session.execute(
        db.select(User).
        where(
            User.uid == session.get("user_uid")
        )).scalar()

    return make_response(render_template("profile/profile.jinja2", user=user))


@blueprint.route("/user/validate_field", methods=["POST"])
@privileges_required_factory(tuple())  # no privileges required, just logged in
def validate_user_field() -> Response:
    """
    Route for AJAX requests to validate field
    """
    field_name = request.json.get("field_name")
    field_value = request.json.get("field_value")
    try:
        validation_method = getattr(User, "validate_" + field_name)
    except AttributeError:
        return make_response(jsonify(f"No such user field to validate: {field_name}"), 400)
    is_valid, criteria = validation_method(field_value)
    return make_response(jsonify({"is_valid": is_valid, "criteria": criteria}), 200)


@blueprint.route("/user/update_field", methods=["POST"])
@privileges_required_factory(tuple())  # no privileges required, just logged in
def update_user_field() -> Response:
    """
    Route for AJAX requests to update user fields
    """
    user = db.session.execute(
        db.select(User).
        where(
            User.uid == session.get("user_uid")
        )).scalar()

    field_name = request.json.get("field_name")
    field_value = request.json.get("field_value")

    response = {}

    try:
        setattr(user, field_name, field_value)
        user.verified = True  # tell the db that there are changes to commit
        db.session.commit()
    except AttributeError:
        response["error"] = [f"No such user field to update: {field_name}"]
        return make_response(jsonify(response), 400)
    except ValueError as e:
        db.session.rollback()
        response["error"] = [key for key in e.args[0].keys() if not e.args[0][key]]
        return make_response(jsonify(response), 400)
    except IntegrityError:
        db.session.rollback()
        if field_name == "username":
            response["error"] = ["Le nom d'utilisateur est déjà pris"]
        elif field_name == "email":
            response["error"] = ["L'adresse email est déjà prise"]
        return make_response(jsonify(response), 400)
    return make_response(jsonify('success'), 200)
