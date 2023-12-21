"""
https://flask.palletsprojects.com/en/2.2.x/templating/#registering-filters

Check list of default Jinja filters
https://jinja.palletsprojects.com/en/3.1.x/templates/#list-of-builtin-filters
"""

from flask import Flask



def reverse_filter(s: list) -> list:
    """
    this is example filter
    {% for x in mylist | reverse %}
    {% endfor %}
    """
    return s[::-1]


# Add your filters
def register_filters(app: Flask) -> Flask:
    """
    Enregistrement des filtres.
    :param app: Application Flask
    :return: Application Flask avec filtres
    """
    app.jinja_env.filters['reverse']: list = reverse_filter

    return app
