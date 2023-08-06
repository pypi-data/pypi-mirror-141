# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modsim']

package_data = \
{'': ['*']}

install_requires = \
['pip>=21.2,<22.0', 'pymodbus[twisted]>=2.5.2,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['modsim = modsim:app']}

setup_kwargs = {
    'name': 'modsim',
    'version': '0.2.1',
    'description': 'A Modbus TCP Device Simulator',
    'long_description': '# ModSim - A Simple Modbus TCP Device Simulator\n\n## Quick Start\n\nA docker image has been provided for user to directly run the program, \n\n  ```bash\n  docker run -p 5020:5020 helloysd/modsim\n  ```\n',
    'author': 'Ying Shaodong',
    'author_email': 'helloysd@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gavinying/modsim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
