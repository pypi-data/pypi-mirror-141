# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['smolqwery', 'smolqwery.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.1.0,<23.0.0',
 'google-cloud-bigquery>=2.34.1,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'rich>=11.2.0,<12.0.0']

setup_kwargs = {
    'name': 'smolqwery',
    'version': '0.1.0',
    'description': 'A Django-oriented tool to make analytics exports to BigQuery',
    'long_description': None,
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@hyperthese.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
