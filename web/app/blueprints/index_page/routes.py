"""
Routes liées à la page d'accueil
"""
from flask import Blueprint, make_response, render_template, Response
from app.blueprints.index_page.views.index import get_plugins

blueprint: Blueprint = Blueprint(
    'index',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@blueprint.route("/", methods=["get"])
def index_route() -> Response:
    """
    Display the index page with the list of plugins
    :return: Index page with plugins
    """
    plugins = get_plugins()
    return make_response(
        render_template(
            "index.jinja2",
            plugins=plugins
        )
    )


# pylint: disable=unused-argument, unnecessary-pass
@blueprint.route("/fuzz-plugin/<slug>", methods=["get"])
def fuzz_plugin_route(slug) -> Response:
    """
    Fuzz a plugin (the function does nothing because it needs to be implemented with the API)
    :param slug: Plugin slug
    """
    pass
