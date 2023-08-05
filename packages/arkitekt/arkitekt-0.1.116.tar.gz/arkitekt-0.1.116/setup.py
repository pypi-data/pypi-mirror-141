# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arkitekt',
 'arkitekt.actors',
 'arkitekt.actors.testing',
 'arkitekt.agents',
 'arkitekt.agents.transport',
 'arkitekt.agents.transport.protocols',
 'arkitekt.api',
 'arkitekt.apps',
 'arkitekt.cli',
 'arkitekt.cli.dev',
 'arkitekt.cli.prod',
 'arkitekt.codegen',
 'arkitekt.definition',
 'arkitekt.fakts',
 'arkitekt.legacy',
 'arkitekt.postmans',
 'arkitekt.postmans.transport',
 'arkitekt.postmans.transport.protocols',
 'arkitekt.structures',
 'arkitekt.structures.serialization',
 'arkitekt.traits',
 'arkitekt.turms']

package_data = \
{'': ['*']}

install_requires = \
['docstring-parser>=0.11',
 'herre>=0.1.65,<0.2.0',
 'inflection>=0.5.1,<0.6.0',
 'janus>=0.6.1,<0.7.0',
 'rath>=0.1.8,<0.2.0',
 'watchdog>=2.1.6,<3.0.0',
 'websockets>=10.0,<11.0']

entry_points = \
{'console_scripts': ['arkitekt = arkitekt.cli.main:entrypoint']}

setup_kwargs = {
    'name': 'arkitekt',
    'version': '0.1.116',
    'description': 'rpc and node backbone',
    'long_description': None,
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
