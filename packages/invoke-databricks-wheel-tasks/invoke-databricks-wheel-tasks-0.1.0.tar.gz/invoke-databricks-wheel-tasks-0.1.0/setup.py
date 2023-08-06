# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['invoke_databricks_wheel_tasks']

package_data = \
{'': ['*']}

install_requires = \
['databricks-cli>=0.16.4,<0.17.0', 'invoke>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'invoke-databricks-wheel-tasks',
    'version': '0.1.0',
    'description': 'Databricks Python Wheel dev tasks in a namespaced collection of tasks to enrich the Invoke CLI task runner.',
    'long_description': None,
    'author': 'Josh Peak',
    'author_email': 'neozenith.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
