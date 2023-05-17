import json
import csv
import sys
import glob
import os


plugin = sys.argv[1]

directory = 'wpgarlic/data/plugin_fuzz_results'

matching_files = glob.glob(directory + '/*' + plugin + '*')
matching_files.sort(key=os.path.getmtime, reverse=True)
file_path = matching_files[0]

with open(file_path) as f:
    data = json.load(f)

data = data["command_results"]

with open('{}.csv'.format(plugin), 'w') as f:
    writer = csv.writer(f)

    writer.writerow(['cmd', 'object_name', 'return_code', 'stdout', 'stderr'])

    for item in data:
        writer.writerow([item['cmd'], item['object_name'], item['return_code'], item['stdout'], item['stderr']])
