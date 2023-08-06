# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tl_scripts']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'ndjson>=0.3.1,<0.4.0',
 'pexpect>=4.8.0,<5.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['copy_kibana_objects = tl_scripts_cli:__main__']}

setup_kwargs = {
    'name': 'tl-scripts',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'dorhar',
    'author_email': 'doron.harnoy@tensorleap.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
