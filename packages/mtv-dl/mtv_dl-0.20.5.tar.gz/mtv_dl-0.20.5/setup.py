# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mtv_dl']
install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'certifi>=2021.10.8,<2022.0.0',
 'docopt>=0.6.2,<0.7.0',
 'durationpy==0.5',
 'iso8601>=0.1.16,<0.2.0',
 'pydash>=4.9.3,<5.0.0',
 'rfc6266>=0.0.4,<0.0.5',
 'rich>=10.11.0,<11.0.0',
 'typing_extensions>=3.10.0.2,<4.0.0.0']

entry_points = \
{'console_scripts': ['mtv_dl = mtv_dl:main']}

setup_kwargs = {
    'name': 'mtv-dl',
    'version': '0.20.5',
    'description': 'MediathekView Downloader',
    'long_description': 'Command line tool to download videos from sources available through MediathekView.\n',
    'author': 'Frank Epperlein',
    'author_email': 'frank+mtv_dl@epperle.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fnep/mtv_dl',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
