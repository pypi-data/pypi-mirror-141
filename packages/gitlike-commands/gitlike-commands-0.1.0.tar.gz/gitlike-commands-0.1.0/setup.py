# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitlike_commands']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gitlike-commands',
    'version': '0.1.0',
    'description': '',
    'long_description': '# gitlike-commands\n\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![GitHub stars](https://img.shields.io/github/stars/unixorn/gitlike-commands.svg)](https://github.com/unixorn/gitlike-commands/stargazers)\n[![Issue Count](https://codeclimate.com/github/unixorn/gitlike-commands/badges/issue_count.svg)](https://codeclimate.com/github/unixorn/gitlike-commands)\n\n## Background\n\n`gitlike-commands` is a python module for easily creating `git`-style subcommand handling.\n\nRefactored out of [thelogrus](https://github.com/unixorn/thelogrus/) so you don\'t have to import any modules that aren\'t part of the Python standard library.\n\n## Usage\n\n`subcommand_driver` automatically figures out what name the script was called as, then looks for subcommands and runs them if found, passing in any command line options.\n\nSo if you have a `foo` script in your `$PATH` as shown below\n\n```python\n#!/usr/bin/env python3\nfrom gitlike_commands import subcommand_driver\n\nif __name__ == \'__main__\':\n    subcommand_driver()\n```\n\nRunning `foo bar baz` will look for a `foo-bar-baz` script, and if present in your `$PATH`, run it. If there is no `foo-bar-baz`, it will look for `foo-bar`, and if it finds that, run `foo-bar baz`.\n\nIf you\'re using poetry in your python project, you can add a gitlike driver as a scripts entry:\n\n```toml\n[tool.poetry.scripts]\ngitalike-demo = "gitlike_commands:subcommand_driver"\n```',
    'author': 'Joe Block',
    'author_email': 'jpb@unixorn.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/unixorn/gitlike-commands',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
