import subprocess

subprocess.run(["git", "clone", "https://github.com/kazet/wpgarlic.git"])
subprocess.run(["cp", "print_findings.py", "wpgarlic/"])
