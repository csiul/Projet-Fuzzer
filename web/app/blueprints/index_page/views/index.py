# Module for getting the list of plugins from the WordPress API
import requests

"""
Get the list of plugins from the WordPress API
"""
def get_plugins():
    base_url = 'https://api.wordpress.org/plugins/info/1.1/'
    r = requests.get(
        base_url +
        '?action=query_plugins&request[page]=1&request[per_page]=250&request[browse]=popular',
        timeout=30)

    results = [plugin for plugin in r.json()['plugins']]

    return results
