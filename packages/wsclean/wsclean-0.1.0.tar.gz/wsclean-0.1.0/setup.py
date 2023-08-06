# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wsclean']

package_data = \
{'': ['*']}

install_requires = \
['pyperclip>=1.8.2,<2.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['wsclean = wsclean.main:app']}

setup_kwargs = {
    'name': 'wsclean',
    'version': '0.1.0',
    'description': 'Cleans the contents of your clipboard by removing redundant whitespace and new lines.',
    'long_description': '# wsclean\n\nReads and adjusts the contents of your clipboard by normalizing the whitespace. Made for the very specific use case of\ncopying content with a lot of erroneous whitespace, like OCR content from cookbooks or textbooks.\n\n## Installation\n\n```sh\npip install wsclean\n```',
    'author': 'Elias Gabriel',
    'author_email': 'me@eliasfgabriel.com',
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
