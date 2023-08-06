# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dw_core', 'dw_datastore', 'dw_datastore.storages', 'dw_query', 'dw_transform']

package_data = \
{'': ['*'], 'dw_core': ['schemas/*']}

install_requires = \
['TakeTheTime>=0.3.1,<0.4.0',
 'appdirs>=1.4.3,<2.0.0',
 'deprecation',
 'iso8601>=0.1.12,<0.2.0',
 'jsonschema>=3.1,<4.0',
 'peewee>=3.0.0,<4.0.0',
 'python-json-logger',
 'strict-rfc3339>=0.7,<0.8',
 'timeslot',
 'tomlkit']

extras_require = \
{'mongo': ['pymongo>=3.10.0,<4.0.0']}

setup_kwargs = {
    'name': 'dw-core',
    'version': '0.0.3',
    'description': 'Core library for DeskWatch',
    'long_description': 'dw-core\n=======\n\n[![GitHub Actions badge](https://github.com/DeskWatch/dw-core/workflows/Build/badge.svg)](https://github.com/DeskWatch/dw-core/actions)\n[![Code coverage](https://codecov.io/gh/DeskWatch/dw-core/branch/master/graph/badge.svg)](https://codecov.io/gh/DeskWatch/dw-core)\n[![PyPI](https://img.shields.io/pypi/v/dw-core)](https://pypi.org/project/dw-core/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Typechecking: Mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n\nCore library for DeskWatch.\n\n\n## Modules\n\n - `dw_core`, contains basic datatypes and utilities, such as the `Event` class, helpers for configuration and logging, as well as schemas for buckets, events, and exports.\n - `dw_datastore`, contains the datastore classes used by dw-server-python.\n - `dw_transform`, all event-transforms used in queries.\n - `dw_query`, the query-language used by DeskWatch.\n\n\n## How to install\n\nTo install the latest git version directly from github without cloning, run\n`pip install git+https://github.com/DeskWatch/dw-core.git`\n\nTo install from a cloned version, cd into the directory and run\n`poetry install` to install inside an virtualenv. If you want to install it\nsystem-wide it can be installed with `pip install .`, but that has the issue\nthat it might not get the exact version of the dependencies due to not reading\nthe poetry.lock file.\n\n',
    'author': 'Kohinoor Bharti',
    'author_email': 'kohinoorbharti7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://deskwatch.net/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
