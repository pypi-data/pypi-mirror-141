# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['propylen']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.1,<0.9.0',
 'click>=8.0.4,<9.0.0',
 'pipenv>=2022.1.8,<2023.0.0',
 'poetry>=1.1.13,<2.0.0',
 'rich>=11.2.0,<12.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['propylen = propylen:cli']}

setup_kwargs = {
    'name': 'propylen',
    'version': '0.4.0',
    'description': 'Python project scaffolding generator',
    'long_description': '# Propylen\n\n__Propylen__ is a Python CLI tool for generating Python projects. In nature, it is a wrapper around pipenv and poetry with some added swag.\n\n__NOTE: Package is not yet fully tested__\n\n# Installation\n\n__Propylen__ should be installed using `pipx` as:\n```shell\npipx install propylen\n```\n\n# Usage\n\n## Initialize project\n\nYou can generate a project structure interactively:\n```shell\npropylen init <project-name>\n```\n\nAlternatively, you can provide necessary infromation in form of command line options. To see available options:\n```shell\npropylen init -h\n```\n## Package Management\n\n__pipenv__ is used as a backend for package management. Options are stripped down.\n\nYou can also use `propylen` to install packages using\n```shell\npropylen install <package-name1> <package-name2> ...\n```\nOr without package name to install dependencies from `Pipfile`\n```shell\npropylen install\n```\n\nAdditional options are also available, to see them:\n```shell\npropylen install -h\n```\n\nYou can uninstall packages using\n```shell\npropylen uninstall <package-name1> <package-name2> ...\n```\n\n## Building\n\n__poetry__ is used as a backend for building. Options are stripped down.\n\nYou can build the project using\n```shell\npropylen build\n```\n\nAdditional options are also available, to see them:\n```shell\npropylen build -h\n```',
    'author': 'Petereon',
    'author_email': 'pvyboch1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/petereon/propylen',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
