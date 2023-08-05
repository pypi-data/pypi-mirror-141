# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepaste']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['dpaste = deepaste.deepaste:main']}

setup_kwargs = {
    'name': 'deepaste',
    'version': '1.0.0',
    'description': 'Deepaste is a simple application to send console pastes to the dpaste.org paste service.',
    'long_description': None,
    'author': 'Lukas Ruzicka',
    'author_email': 'lruzicka@redhat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
