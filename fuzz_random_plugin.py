import requests
from subprocess import call
import os
import random
import fuzz_plugin
import shutil
import os

# quickly patch the installation

fuzzer_container_file = 'fuzzer_container.py'
docker_compose_file = 'docker-compose.yml'

with open(fuzzer_container_file, 'r') as file:
    lines = file.readlines()

current_folder = os.path.basename(os.getcwd())
if lines[152] != f'    network_name = "{current_folder}_network2"':
    lines[152] = f'    network_name = "{current_folder}_network2"'

    print(f"changed line 152 of {fuzzer_container_file}")
    with open(fuzzer_container_file, 'w') as file:
        file.writelines(lines)

with open(docker_compose_file, 'r') as file:
    lines = file.readlines()

if lines[18].strip() == 'container_name: wordpress1':
    del lines[18]

    print(f"deleted line 19 of {docker_compose_file}")
    with open(docker_compose_file, 'w') as file:
        file.writelines(lines)


# Set the API endpoint and parameters
endpoint = "https://api.wordpress.org/plugins/info/1.2/"
params = {
    "action": "query_plugins",
    "request[per_page]": 250,  # number of plugins per page
    "request[page]": random.randint(0, 222),  # page number # there was 222+1 pages last time I checked
}

# Make the API request and retrieve the response
response = requests.get(endpoint, params=params)
data = response.json()

# Start fuzzing a random plugin
max_index = len(data["plugins"])
plugin = data["plugins"][random.randint(0, max_index-1)]
fuzz_plugin.fuzz_plugin(plugin['slug'])