"""
Router : WordPress
"""
from math import ceil
from random import randint

import requests
from fastapi import APIRouter, HTTPException, Request

BASE_URL = "https://api.wordpress.org/plugins/info/1.2/"

router = APIRouter(prefix="/wordpress", tags=['wordpress'])


@router.get('/plugins')
def get_plugins(request: Request, browse: str = 'popular', page: int = 1):
    """
    Obtient la liste des plugins WordPress.
    Agit comme proxy vers le site officiel wordpress.org.
    ATTENTION, cette requête n'est présentement pas optimisée, 1.8 minutes pour obtenir la liste complète.
    """
    params = {
        "action": "query_plugins",
        "request[per_page]": 250,  # number of plugins per page
        "request[page]": page,
        "request[browse]": browse
    }
    response = requests.get(BASE_URL, params=params, timeout=30)
    if response.status_code != 200:
        raise HTTPException(status_code=502,
                            detail={
                                'msg': 'wordpress.org responded with an unexpected status_code.',
                                'status_code': response.status_code,
                                'response': response.text
                            })
    data = response.json()

    if page < 1 or page > int(data['info']['pages']):
        raise HTTPException(status_code=403, detail=f'Page number must be between 1 and {int(data["info"]["pages"])}.')

    return {
        'data': data['plugins'],
        'count': len(data['plugins']),
        'total': data['info']['results'],
        'pages': data['info']['pages'],
        'next': f'{request.url.replace_query_params(browse=browse, page=page + 1)}' if page < int(data['info']['pages'])
        else None
    }


@router.get('/plugins_count')
def get_plugins_count():
    """
    Obtient le nombre total de plugins.
    """
    params = {"action": "query_plugins"}
    response = requests.get(BASE_URL, params=params, timeout=30)
    if response.status_code != 200:
        raise HTTPException(status_code=502,
                            detail={
                                'msg': 'wordpress.org responded with an unexpected status_code.',
                                'status_code': response.status_code,
                                'response': response.text
                            })
    data = response.json()
    info = data['info']['results']
    return {
        'count': info
    }


@router.get('/random_plugin',
            summary='Get a random plugin',
            description='Get a random plugin on wordpress.org. `random.randint` is used to generate a random index.')
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


@router.get('/check/{plugin_name}')
def check_if_plugin_exists(plugin_name: str):
    """
    Vérifie si un plugin existe sur wordpress.org.
    :param plugin_name: Nom du plugin à vérifier
    :return: 404 si le plugin n'existe pas, 200 si trouvé, avec l'objet JSON
    """
    params = {
        "action": "plugin_information",
        "request[slug]": plugin_name
    }
    response = requests.get(BASE_URL, params=params, timeout=30)
    if response.status_code not in [200, 404]:
        raise HTTPException(status_code=502,
                            detail={
                                'msg': 'wordpress.org responded with an unexpected status_code.',
                                'status_code': response.status_code,
                                'response': response.text
                            })
    data = response.json()
    if data.get('error', '') == 'Plugin not found.':
        raise HTTPException(status_code=404, detail='Plugin not found on wordpress.org')
    return data
