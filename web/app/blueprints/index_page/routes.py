"""
Routes liées à la page d'accueil
"""
from flask import Blueprint, make_response, render_template, Response, redirect, url_for, jsonify
from app.blueprints.index_page.views.index import get_plugins, get_plugins_count, fuzz_plugin, get_fuzzer_state, get_already_fuzzed_plugins, get_api_status, get_random_plugin
import requests

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
    plugins_count = get_plugins_count()
    fuzzer_state = get_fuzzer_state()
    already_fuzzed_plugins = get_already_fuzzed_plugins()
    api_status = get_api_status()
    return make_response(
        render_template(
            "index.jinja2",
            plugins=plugins,
            plugins_count=plugins_count,
            fuzzer_state=fuzzer_state,
            already_fuzzed_plugins=already_fuzzed_plugins,
            api_status=api_status
        )
    )


# pylint: disable=unused-argument, unnecessary-pass
@blueprint.route("/fuzz-plugin/<slug>", methods=["get"])
def fuzz_plugin_route(slug) -> Response:
    """
    Fuzz a plugin
    :param slug: Plugin slug
    """
    message = fuzz_plugin(slug)
    return redirect(url_for('index.index_route'))


@blueprint.route("/download-plugin-results/<slug>", methods=["get"])
def download_plugin_results_route(slug) -> Response:
    """
    Download the results of a fuzzed plugin
    :param slug: Plugin slug
    """
    base_url = 'http://host.docker.internal:5050/'

    r = requests.get(
        base_url + 'download_plugin_results/' + slug,
        timeout=30)
    results = r.json()['results']

    return make_response(
        render_template(
            "plugin_results.jinja2",
            results=results
        )
    )


@blueprint.route("/random-plugin", methods=["get"])
def random_plugin_route() -> Response:
    """
    Get a random plugin
    """
    random_plugin = get_random_plugin()

    return jsonify({
        'name': random_plugin['name'],
        'short_description': random_plugin['short_description'],
        'added': random_plugin['added'],
        'last_updated': random_plugin['last_updated'],
        'slug': random_plugin['slug']
    })


@blueprint.route("/search-plugin/<slug>", methods=["get"])
def search_plugin_route(slug) -> Response:
    """
    Search a plugin
    :param slug: Plugin slug
    """
    base_url = 'http://host.docker.internal:5050/'

    r = requests.get(
        base_url + 'wordpress/check/' + slug,
        timeout=30)
    plugin = r.json()

    if r.status_code == 404:
        return jsonify({
            'exists': False
        })
    else:
        if plugin.get('short_description'):
            short_description = plugin['short_description']
        else:
            short_description = 'No description'
        
        return jsonify({
            'exists': True,
            'name': plugin['name'],
            'short_description': short_description,
            'added': plugin['added'],
            'last_updated': plugin['last_updated'],
            'slug': plugin['slug']
        })