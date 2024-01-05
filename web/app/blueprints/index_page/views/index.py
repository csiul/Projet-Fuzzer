"""
Module for getting the list of plugins from the WordPress API
"""
import requests


def get_plugins():
    """
    Get the list of plugins from the API
    :return: List of plugins
    """
    base_url = 'http://host.docker.internal:5050/'

    r = requests.get(
        base_url + 'wordpress/plugins',
        timeout=30)
    results = [plugin for plugin in r.json()['data']]

    return results


def get_plugins_count():
    """
    Get the number of plugins from the API
    :return: Number of plugins
    """
    base_url = 'http://host.docker.internal:5050/'

    r = requests.get(
        base_url + 'wordpress/plugins_count',
        timeout=30)
    count = r.json()['count']

    return count


def fuzz_plugin(slug):
    """
    Fuzz a plugin
    :param slug: Plugin slug
    """
    base_url = 'http://host.docker.internal:5050/'

    r = requests.post(
        base_url + 'fuzz_plugin/' + slug,
        timeout=30)
    
    message = r.json()['message']

    return message


def get_fuzzer_state():
    """
    Get the fuzzer state
    :return: Fuzzer state
    """
    base_url = 'http://host.docker.internal:5050/'

    r = requests.get(
        base_url + 'fuzz_plugin/state',
        timeout=30)
    state = r.json()

    return state


def get_already_fuzzed_plugins():
    """
    Get the list of already fuzzed plugins
    :return: List of already fuzzed plugins
    """
    base_url = 'http://host.docker.internal:5050/'

    r = requests.get(
        base_url + 'fuzz_plugin/history',
        timeout=30)
    already_fuzzed_plugins = r.json()['data']

    return already_fuzzed_plugins


def get_api_status():
    """
    Get the API status
    :return: API status
    """
    base_url = 'http://host.docker.internal:5050/'

    r = requests.get(
        base_url + 'status',
        timeout=30)
    api_status = r.json()['result']

    return api_status


def get_random_plugin():
    """
    Get a random plugin
    :return: Random plugin
    """
    base_url = 'http://host.docker.internal:5050/'

    r = requests.get(
        base_url + 'wordpress/random_plugin',
        timeout=30)
    random_plugin = r.json()

    return random_plugin