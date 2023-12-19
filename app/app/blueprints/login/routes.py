from flask import Blueprint, current_app, render_template, session, request


# do not rename "blueprint" variable if you want to use auto import
blueprint: Blueprint = Blueprint(
    'login',
    __name__,
    template_folder='templates'
)


@blueprint.route("/login", methods=["GET", "POST"])
def login_route() -> str:
    # current_app.config.get("MY_CONFIG_VARIABLE")
    # context: dict = {
    #     "hello": "world"
    # }
    if request.method == "POST":
        session["email"] = request.form.get("email")

    return render_template(
        "login.jinja2"
    )
