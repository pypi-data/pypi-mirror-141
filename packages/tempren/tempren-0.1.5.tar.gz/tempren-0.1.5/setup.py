# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tempren', 'tempren.tags', 'tempren.template', 'tempren.template.grammar']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.2.0,<2.0.0',
 'antlr4-python3-runtime>=4.9.2,<5.0.0',
 'pathvalidate>=2.4.1,<3.0.0',
 'pydantic>=1.8.1,<2.0.0']

entry_points = \
{'console_scripts': ['tempren = tempren.cli:main']}

setup_kwargs = {
    'name': 'tempren',
    'version': '0.1.5',
    'description': 'Template-based renaming utility',
    'long_description': '# [WIP] Tempren - template-based batch file renaming utility\n[![Build Status](https://travis-ci.org/idle-code/tempren.svg?branch=develop)](https://travis-ci.org/idle-code/tempren)\n[![codecov](https://codecov.io/gh/idle-code/tempren/branch/develop/graph/badge.svg?token=1CR2PX6GYB)](https://codecov.io/gh/idle-code/tempren)\n\n**This project is currently in a Work-In-Progress stage so if you are looking for working solution... keep looking.**\n\nTODO: Summary\n\n## Features\n- Template-based filename/path generation\n- Configurable file selection\n- Metadata-based sorting\n\n\n## Install\n```console\n$ pip install [--user] poetry\n$ poetry install\n```\n\n## TODO: Usage\n\n**Note: When playing with tempren make sure to use `--dry-run` (`-d`) flag so that the actual files are not accidentally changed.**\n\nTempren have two main modes of operation: **name** and **path**.\n\nIn the **name** mode, the template is used for filename generation only.\nThis is useful if you want to operate on files specified on the command line or in a single directory.\n\nWith **path** mode, the template generates a whole path (relative to the input directory).\nThis way you can sort files into dynamically generated catalogues.\n### Template syntax\n#### Pipe list sugar\n### Name mode\n### Path mode\n### Filtering\n#### Glob filtering\n#### Regex filtering\n#### Template filtering\n#### Case sensitiveness and filter inversion\n### Sorting\n\n### Testing\nTests are written with a help of [pytest](https://docs.pytest.org/en/latest/). Just enter repository root and run:\n```console\n$ pytest\n```\n\n## Contribution\nCode conventions are enforced via [pre-commit](https://pre-commit.com/). It is listed in development depenencies so if you are able to run tests - you should have it installed too.\nTo get started you will still need to install git hooks via:\n```console\n$ pre-commit install\n```\nNow every time you invoke `git commit` a series of cleanup scripts will run and modify your patchset.\n\n### TODO: Tags development\n',
    'author': 'Paweł Żukowski',
    'author_email': 'p.z.idlecode@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/idle-code/tempren',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
