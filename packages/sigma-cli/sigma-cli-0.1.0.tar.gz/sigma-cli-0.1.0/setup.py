# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigma', 'sigma.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'prettytable>=3.1.1,<4.0.0',
 'pysigma-backend-splunk>=0.1.1,<0.2.0',
 'pysigma-pipeline-crowdstrike>=0.1.0,<0.2.0',
 'pysigma-pipeline-sysmon>=0.1.0,<0.2.0',
 'pysigma>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['sigma = sigma.cli.main:main']}

setup_kwargs = {
    'name': 'sigma-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Sigma Command Line Interface\n\n![Tests](https://github.com/SigmaHQ/sigma-cli/actions/workflows/test.yml/badge.svg)\n![Coverage Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/thomaspatzke/0c868df261d4a5d5a1dafe71b1557d69/raw/SigmaHQ-sigma-cli.json)\n![Status](https://img.shields.io/badge/Status-pre--release-orange)\n\nThis is the Sigma command line interface using the [pySigma](https://github.com/SigmaHQ/pySigma) library to manage, list\nand convert Sigma rules into query languages.\n\n## Getting Started\n\ntbd\n\n## Maintainers\n\nThe project is currently maintained by:\n\n- Thomas Patzke <thomas@patzke.org>',
    'author': 'Thomas Patzke',
    'author_email': 'thomas@patzke.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SigmaHQ/sigma-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
