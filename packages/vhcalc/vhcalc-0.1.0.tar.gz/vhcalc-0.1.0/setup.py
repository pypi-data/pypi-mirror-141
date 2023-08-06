# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vhcalc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'vhcalc',
    'version': '0.1.0',
    'description': "It's a client-side library that implements a custom algorithm for extracting video hashes (fingerprints) from any video source.",
    'long_description': "[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square)](https://conventionalcommits.org)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Github Actions](https://github.com/yoyonel/vhcalc/actions/workflows/python-check.yaml/badge.svg)](https://github.com/yoyonel/vhcalc/wayback-machine-saver/actions/workflows/python-check.yaml)\n\n[![PyPI Package latest release](https://img.shields.io/pypi/v/vhcalc.svg?style=flat-square)](https://pypi.org/project/vhcalc/)\n[![PyPI Package download count (per month)](https://img.shields.io/pypi/dm/vhcalc?style=flat-square)](https://pypi.org/project/vhcalc/)\n[![Supported versions](https://img.shields.io/pypi/pyversions/vhcalc.svg?style=flat-square)](https://pypi.org/project/vhcalc/)\n\n\n# vhcalc\n\nIt's a client-side library that implements a custom algorithm for extracting video hashes (fingerprints) from any video source.\n\n## Getting Started\n\n### Prerequisites\n* [Python](https://www.python.org/downloads/)\n\n## Usage\n\n\n## Contributing\nSee [Contributing](contributing.md)\n\n## Authors\nLionel Atty <yoyonel@hotmail.com>\n\n\nCreated from [Lee-W/cookiecutter-python-template](https://github.com/Lee-W/cookiecutter-python-template/tree/1.1.2) version 1.1.2\n",
    'author': 'Lionel Atty',
    'author_email': 'yoyonel@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yoyonel/vhcalc',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
