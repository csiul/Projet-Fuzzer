"""
Router : WordPress
"""
from math import ceil
from random import randint

import requests
from fastapi import APIRouter

BASE_URL = "https://api.wordpress.org/plugins/info/1.2/"

router = APIRouter(prefix="/wordpress", tags=['wordpress'])


@router.get('/plugins')
def get_plugins():
    """
    Obtient la liste des plugins WordPress.
    Agit comme proxy vers le site officiel wordpress.org.
    ATTENTION, cette requête n'est présentement pas optimisée, 1.8 minutes pour obtenir la liste complète.
    """
    page = 1
    plugins = []
    while True:
        params = {
            "action": "query_plugins",
            "request[per_page]": 250,  # number of plugins per page
            "request[page]": page
        }
        response = requests.get(BASE_URL, params=params, timeout=30)
        data = response.json()
        plugins += data['plugins']
        if page < data['info']['pages']:
            page += 1
        else:
            break
    return plugins


@router.get('/plugins_count')
def get_plugins_count():
    """
    Obtient le nombre total de plugins.
    """
    params = {"action": "query_plugins"}
    response = requests.get(BASE_URL, params=params, timeout=30)
    data = response.json()
    info = data['info']['results']
    return {
        'count': info
    }


@router.get('/random_plugin')
def get_random_plugin():
    """
    Obtient un plugin aléatoire parmis les ~5K plugins de WordPress.org.
    """
    total = get_plugins_count()['count']
    i = randint(1, total)
    page = ceil(i / 250.0)
    params = {
        "action": "query_plugins",
        "request[per_page]": 250,  # number of plugins per page
        "request[page]": page
    }
    response = requests.get(BASE_URL, params=params, timeout=30)
    data = response.json()
    plugin = data['plugins'][i - 250 * (page - 1) - 1]
    return plugin
