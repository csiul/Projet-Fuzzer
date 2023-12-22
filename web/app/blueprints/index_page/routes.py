from flask import Blueprint, make_response, render_template, current_app, Response

from app.blueprints.index_page.views.index import get_plugins

blueprint: Blueprint = Blueprint(
    'index',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@blueprint.route("/", methods=["get"])
def index_route() -> Response:
    plugins = get_plugins()
    return make_response(
        render_template(
            "index.jinja2",
            plugins=plugins
        )
    )


@blueprint.route("/fuzz-plugin/<slug>", methods=["get"])
def fuzz_plugin_route(slug) -> Response:
    pass

