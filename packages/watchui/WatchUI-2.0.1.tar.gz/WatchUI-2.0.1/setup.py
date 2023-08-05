# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['WatchUI', 'WatchUI.Ibasic', 'WatchUI.keywords']

package_data = \
{'': ['*']}

install_requires = \
['Pillow',
 'PyMuPDF',
 'imutils',
 'numpy',
 'opencv-python',
 'pandas',
 'pytesseract',
 'robotframework',
 'scikit-image',
 'scikit-learn']

entry_points = \
{'console_scripts': ['docs = tasks:docs', 'test = tasks:test']}

setup_kwargs = {
    'name': 'watchui',
    'version': '2.0.1',
    'description': 'RobotFramework library package for automated visual testing.',
    'long_description': None,
    'author': 'Jan Egermaier',
    'author_email': 'jan.egermaier@tesena.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
