# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sdf_heroku_deploy']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['sdfh_cli = sdf_heroku_deploy.sdfh_cli:cli']}

setup_kwargs = {
    'name': 'sdf-heroku-deploy',
    'version': '2.0.0',
    'description': 'This script generates a Dockerfile with the basic settings to deploy your flask application to heroku. And as a bonus a steps.txt with the step by step for you to publish the project.',
    'long_description': '\n# Project Description\n\nThis script generates a Dockerfile with the basic settings to deploy your flask application to heroku. And as a bonus a `steps.txt` with the step by step for you to publish the project.\n\n\n# Note: Run the script inside your project folder.\n\n## Installation from Pypi\n`pip install sdf-heroku-deploy`\n\n## Module Usage\n\n```python\nfrom sdf_heroku_deploy import main\nmain()\n```\n\n\n## CLI Usage\n\n### Get the list of available commands\n\n`sdfh_cli --help`\n\nOutput \n\n```\nOptions:\n  -img, --image_name TEXT       Type the name of the image you want to give   \n                                the image to be created.\n  -hap, --heroku_app_name TEXT  Type the name of the heroku app you want to   \n                                give the app to be created.\n  -r, --run TEXT                Type the name of the file that runs your flask\n                                application.\n  --help                        Show this message and exit.\n```\n##  Commands usage example\n\n1. `sdfh_cli -img my_docker_image -hap my_heroku_app_name -r flask_app_runner`\n\n2. `sdfh_cli --image_name my_docker_image --heroku_app_name my_heroku_app_name --run flask_app_runner`\n\nOutput \n```\n./Dockerfile\n./steps.txt\n```\n',
    'author': 'Matheus Santos',
    'author_email': '78329418+darkmathew@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/darkmathew/simple-docker-flask-deploy-to-heroku',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
