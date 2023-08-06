# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tvdb_api_client']

package_data = \
{'': ['*']}

install_requires = \
['pathurl>=0.5.0,<0.6.0', 'requests>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'tvdb-api-client',
    'version': '0.6.0',
    'description': 'A python client for TVDB rest API',
    'long_description': '===============================================\ntvdb_api_client: an unofficial API for the TVDB\n===============================================\n\n.. image:: https://github.com/spapanik/tvdb_api_client/actions/workflows/build.yml/badge.svg\n  :alt: Build\n  :target: https://github.com/spapanik/tvdb_api_client/actions/workflows/build.yml\n.. image:: https://img.shields.io/lgtm/alerts/g/spapanik/tvdb_api_client.svg\n  :alt: Total alerts\n  :target: https://lgtm.com/projects/g/spapanik/tvdb_api_client/alerts/\n.. image:: https://img.shields.io/github/license/spapanik/tvdb_api_client\n  :alt: License\n  :target: https://github.com/spapanik/tvdb_api_client/blob/main/LICENSE.txt\n.. image:: https://img.shields.io/pypi/v/tvdb_api_client\n  :alt: PyPI\n  :target: https://pypi.org/project/tvdb_api_client\n.. image:: https://pepy.tech/badge/tvdb-api-client\n  :alt: Downloads\n  :target: https://pepy.tech/project/tvdb-api-client\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :alt: Code style\n  :target: https://github.com/psf/black\n\n``tvdb_api_client`` is an unofficial API for the TVDB.\n\nIn a nutshell\n-------------\n\nInstallation\n^^^^^^^^^^^^\n\nThe easiest way is to use `poetry`_ to manage your dependencies and add *tvdb_api_client* to them.\n\n.. code-block:: toml\n\n    [tool.poetry.dependencies]\n    tvdb_api_client = "*"\n\nUsage\n^^^^^\n\nInitialise the client (example using the django cache):\n\n.. code:: python\n\n    from django.core.cache import cache\n    from tvdb_api_client import TVDBClient\n\n    client = TVDBClient("username", "user_key", "api_key", cache)\n\nOnce the client has been initialised, you can use it to get the following info:\n\n* get TV series by TVDB id\n* get TV series by IMDb id\n* find identifying info for a TV series by its name\n* get episodes by TV series using its TVDB id\n\nLinks\n-----\n\n- `Documentation`_\n- `Changelog`_\n\n\n.. _poetry: https://python-poetry.org/\n.. _Changelog: https://github.com/spapanik/tvdb_api_client/blob/main/CHANGELOG.rst\n.. _Documentation: https://tvdb-api-client.readthedocs.io/en/latest/\n',
    'author': 'Stephanos Kuma',
    'author_email': 'stephanos@kuma.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spapanik/tvdb_api_client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
