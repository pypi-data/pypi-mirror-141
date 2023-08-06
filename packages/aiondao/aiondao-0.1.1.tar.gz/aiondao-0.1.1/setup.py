# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiondao',
 'aiondao.agents',
 'aiondao.interfaces',
 'aiondao.libs',
 'aiondao.policies',
 'aiondao.utils']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'Mesa>=0.9.0,<0.10.0',
 'addict>=2.4.0,<3.0.0',
 'auto-all>=1.4.1,<2.0.0',
 'cadCAD>=0.4.28,<0.5.0',
 'celery[redis]>=5.2.3,<6.0.0',
 'cytoolz>=0.11.2,<0.12.0',
 'decorator>=5.1.1,<6.0.0',
 'devtools>=0.8.0,<0.9.0',
 'fastapi>=0.74.1,<0.75.0',
 'keyring>=23.5.0,<24.0.0',
 'libcst>=0.4.1,<0.5.0',
 'loguru>=0.6.0,<0.7.0',
 'networkx>=2.6.3,<3.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'scipy>=1.8.0,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer>=0.4.0,<0.5.0',
 'wrapt>=1.13.3,<2.0.0']

entry_points = \
{'console_scripts': ['aiondao = aiondao.cli:app']}

setup_kwargs = {
    'name': 'aiondao',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'kivo360',
    'author_email': 'kivo360@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
