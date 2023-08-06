# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['task_api', 'task_api.backends', 'task_api.migrations']

package_data = \
{'': ['*'], 'task_api': ['static/*']}

install_requires = \
['Django', 'celery>=4', 'djangorestframework>=3.0,<4.0', 'six>=1.16.0,<2.0.0']

setup_kwargs = {
    'name': 'django-task-api',
    'version': '1.4.1',
    'description': 'A REST API for managing background tasks in Django',
    'long_description': None,
    'author': 'Nikolas Stevenson-Molnar',
    'author_email': 'nik.molnar@consbio.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
