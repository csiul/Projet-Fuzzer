import requests
from subprocess import call
import os
import random

# Set the API endpoint and parameters
endpoint = "https://api.wordpress.org/plugins/info/1.2/"
params = {
    "action": "query_plugins",
    "request[per_page]": 250,  # number of plugins per page
    "request[page]": 1,  # page number
}

# Make the API request and retrieve the response
response = requests.get(endpoint, params=params)
data = response.json()

# Start fuzzing a random plugin
max_index = len(data["plugins"])
plugin = data["plugins"][random.randint(0, max_index-1)]
os.system(f"fuzz_plugin.py {plugin['slug']} --version {plugin['version']}")