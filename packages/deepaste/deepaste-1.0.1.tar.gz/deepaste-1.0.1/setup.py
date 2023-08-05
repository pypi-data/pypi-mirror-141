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
    'version': '1.0.1',
    'description': 'Deepaste is a simple application to send console pastes to the dpaste.org paste service.',
    'long_description': '# DPASTE -- a CLI paste tool\n\nThis script can help you paste content from the CLI onto a web service at `dpaste.de`.\n\n## Usage\n\n### Paste one liners\n\n`dpaste --content <content> --expire <time> --lexer <content_type>`\n\n### Pase a file content\n\n`dpaste --file <file> --expire <time> --lexer <content_type>`\n\n### Using a pipe to send pastes\n\nYou can also use a pipe to send text to dpaste, for example\n\n`journalctl -b | dpaste`\n\nWhen successful, the link to the pasted content will be printed to the console.\n\n## Variables\n\n### Expiration time\n\nThis variable sets how long the page will keep your snippet. You can use:\n\n* onetime (This will let you display once.)\n* hour (default)\n* day\n* week\n\n### Content type (lexer)\n\nThis variable tells the engine how to highlight the content.\n\n* _text (default)\n* bash\n* c\n* html\n* perl\n* python\n* java\n* rst\n* tex\n* vim\n\nMore can be seen [in the Dpaste documentaton](https://dpaste.readthedocs.io/en/latest/index.html).\n\n## Example\n\nWhen you have a python script `program.py` and you want to paste it for a *week*, with *Python* highlighting, do:\n\n`dpaste --file program.py --expire week --lexer python`\n\nYou can also use `-f`, `-e`, and `-l` shortcuts to provide arguments.\n',
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
