"""
Installation de wpgarlic
"""

import subprocess

subprocess.run(["git", "clone", "https://github.com/kazet/wpgarlic.git"], check=False)
subprocess.run(["cp", "print_findings.py", "wpgarlic/"], check=False)
