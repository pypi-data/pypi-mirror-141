# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rpg_handbook', 'rpg_handbook.commands']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=8.0.4,<9.0.0',
 'subtitle-filter>=1.4.3,<2.0.0',
 'tqdm>=4.63.0,<5.0.0']

extras_require = \
{'docs': ['Sphinx>=4.4.0,<5.0.0',
          'furo>=2022.3.4,<2023.0.0',
          'm2r2>=0.3.2,<0.4.0',
          'sphinxcontrib-images>=0.9.4,<0.10.0']}

entry_points = \
{'console_scripts': ['rpg = rpg_handbook.__main__:main']}

setup_kwargs = {
    'name': 'rpg-handbook',
    'version': '0.1.0',
    'description': 'Peer-to-Peer DVD Remuxing Rules by -RPG.',
    'long_description': None,
    'author': 'rlaphoenix',
    'author_email': 'rlaphoenix@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rlaphoenix/RPG',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
