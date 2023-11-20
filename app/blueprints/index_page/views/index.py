import requests

def get_plugins():
    r = requests.get('https://api.wordpress.org/plugins/info/1.1/?action=query_plugins&request[page]=1&request[per_page]=250&request[browse]=popular')

    results = [plugin["slug"] for plugin in r.json()['plugins']]

    return results
