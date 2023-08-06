# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['yashiro']

package_data = \
{'': ['*']}

install_requires = \
['dj-settings>=2.0.0,<3.0.0', 'jinja2>=3.0.0,<4.0.0']

entry_points = \
{'console_scripts': ['yashiro = yashiro.main:write_output']}

setup_kwargs = {
    'name': 'yashiro',
    'version': '0.9.0',
    'description': 'A cli template tool based on jinja',
    'long_description': '===========================================\nyashiro: A template CLI tool based on jinja\n===========================================\n\n.. image:: https://github.com/spapanik/yashiro/actions/workflows/build.yml/badge.svg\n  :alt: Build\n  :target: https://github.com/spapanik/yashiro/actions/workflows/build.yml\n.. image:: https://img.shields.io/lgtm/alerts/g/spapanik/yashiro.svg\n  :alt: Total alerts\n  :target: https://lgtm.com/projects/g/spapanik/yashiro/alerts/\n.. image:: https://img.shields.io/github/license/spapanik/yashiro\n  :alt: License\n  :target: https://github.com/spapanik/yashiro/blob/main/LICENSE.txt\n.. image:: https://img.shields.io/pypi/v/yashiro\n  :alt: PyPI\n  :target: https://pypi.org/project/yashiro\n.. image:: https://pepy.tech/badge/yashiro\n  :alt: Downloads\n  :target: https://pepy.tech/project/yashiro\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :alt: Code style\n  :target: https://github.com/psf/black\n\n``yashiro`` is just a thin wrapper around jinja.\n\nIn a nutshell\n-------------\n\nInstallation\n^^^^^^^^^^^^\n\nThe easiest way is to use `poetry`_ to manage your dependencies and add *yashiro* to them.\n\n.. code-block:: toml\n\n    [tool.poetry.dependencies]\n    yashiro = "*"\n\nUsage\n^^^^^\n\n``yashiro``, once installed offers a single command, ``yashiro``, that parses the templated based on a JSON file. ``yashiro`` follows the GNU recommendations for command line interfaces, and offers:\n\n* ``-h`` or ``--help`` to print help, and\n* ``-V`` or ``--version`` to print the version\n\nYou can use yashiro to parse a template.\n\n.. code:: console\n\n    usage: yashiro [-h] [-V] [-m MAPPING] [-s] -t TEMPLATE\n\n    optional arguments:\n        -h, --help             Show this help message and exit\n        -m/--mappings MAPPINGS The path to the file that contains the mappings\n        -t/--template TEMPLATE The path to the template\n        -V/--version           Print the version and exit\n\nLinks\n-----\n\n- `Documentation`_\n- `Changelog`_\n\n\n.. _poetry: https://python-poetry.org/\n.. _Changelog: https://github.com/spapanik/yashiro/blob/main/CHANGELOG.rst\n.. _Documentation: https://yashiro.readthedocs.io/en/latest/\n',
    'author': 'Stephanos Kuma',
    'author_email': 'stephanos@kuma.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spapanik/yashiro',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
