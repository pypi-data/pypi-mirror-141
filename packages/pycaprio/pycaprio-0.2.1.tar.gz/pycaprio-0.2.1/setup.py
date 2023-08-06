# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycaprio',
 'pycaprio.core',
 'pycaprio.core.adapters',
 'pycaprio.core.clients',
 'pycaprio.core.interfaces',
 'pycaprio.core.objects',
 'pycaprio.core.schemas']

package_data = \
{'': ['*']}

install_requires = \
['requests', 'requests-toolbelt>=0.9.1,<0.10.0']

setup_kwargs = {
    'name': 'pycaprio',
    'version': '0.2.1',
    'description': 'Python client for the INCEpTION annotation tool API',
    'long_description': None,
    'author': 'Javier Luna Molina',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
