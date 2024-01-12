"""
This module contains all routes related to admin pages and related processes
"""
from flask import Blueprint, render_template, Response, make_response, request, jsonify
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
    if request.method == "POST":
        user_data_fields = ("username", "email", "last_name", "first_name", "password")
        user_data = {field: request.json.get(field) for field in user_data_fields}
        response = {}
        if any([user_data[field] is None for field in user_data_fields]):
            response['success_status'] = False
            response['message'] = "Missing required fields"
            response['user_data'] = user_data
            return make_response(jsonify(response), 400)
        try:
            user = User(**user_data)
            db.session.add(user)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            response['success_status'] = False
            response['message'] = "An error occurred while creating the user"
            response['errors'] = e.args[0]
            response['user_data'] = user_data
            return make_response(jsonify(response), 200)
        except IntegrityError:
            db.session.rollback()
            response['success_status'] = False
            response['message'] = "Username or email already exists"
            response['user_data'] = user_data
            return make_response(jsonify(response), 200)
        response['success_status'] = True
        response['message'] = "User created successfully"
        response['user_data'] = user_data
        return make_response(jsonify(response), 200)

    return make_response(render_template("admin/register.jinja2"))


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
