pip install --root-user-action=ignore pylint > /dev/null 2>&1
pylint $(find . -name '*.py')
pip uninstall -y --root-user-action=ignore pylint > /dev/null 2>&1