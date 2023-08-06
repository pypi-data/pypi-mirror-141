===========================================
yashiro: A template CLI tool based on jinja
===========================================

.. image:: https://github.com/spapanik/yashiro/actions/workflows/build.yml/badge.svg
  :alt: Build
  :target: https://github.com/spapanik/yashiro/actions/workflows/build.yml
.. image:: https://img.shields.io/lgtm/alerts/g/spapanik/yashiro.svg
  :alt: Total alerts
  :target: https://lgtm.com/projects/g/spapanik/yashiro/alerts/
.. image:: https://img.shields.io/github/license/spapanik/yashiro
  :alt: License
  :target: https://github.com/spapanik/yashiro/blob/main/LICENSE.txt
.. image:: https://img.shields.io/pypi/v/yashiro
  :alt: PyPI
  :target: https://pypi.org/project/yashiro
.. image:: https://pepy.tech/badge/yashiro
  :alt: Downloads
  :target: https://pepy.tech/project/yashiro
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :alt: Code style
  :target: https://github.com/psf/black

``yashiro`` is just a thin wrapper around jinja.

In a nutshell
-------------

Installation
^^^^^^^^^^^^

The easiest way is to use `poetry`_ to manage your dependencies and add *yashiro* to them.

.. code-block:: toml

    [tool.poetry.dependencies]
    yashiro = "*"

Usage
^^^^^

``yashiro``, once installed offers a single command, ``yashiro``, that parses the templated based on a JSON file. ``yashiro`` follows the GNU recommendations for command line interfaces, and offers:

* ``-h`` or ``--help`` to print help, and
* ``-V`` or ``--version`` to print the version

You can use yashiro to parse a template.

.. code:: console

    usage: yashiro [-h] [-V] [-m MAPPING] [-s] -t TEMPLATE

    optional arguments:
        -h, --help             Show this help message and exit
        -m/--mappings MAPPINGS The path to the file that contains the mappings
        -t/--template TEMPLATE The path to the template
        -V/--version           Print the version and exit

Links
-----

- `Documentation`_
- `Changelog`_


.. _poetry: https://python-poetry.org/
.. _Changelog: https://github.com/spapanik/yashiro/blob/main/CHANGELOG.rst
.. _Documentation: https://yashiro.readthedocs.io/en/latest/
