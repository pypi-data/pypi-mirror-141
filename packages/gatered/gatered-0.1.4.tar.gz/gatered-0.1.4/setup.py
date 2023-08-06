# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gatered']

package_data = \
{'': ['*']}

install_requires = \
['aiometer>=0.3.0,<0.4.0',
 'httpx[http2]>=0.22.0,<0.23.0',
 'python-dotenv>=0.19.2,<0.20.0']

setup_kwargs = {
    'name': 'gatered',
    'version': '0.1.4',
    'description': 'Reddit Gateway API Library',
    'long_description': '# GateRed -- Reddit Gateway API Library\n\n[![CI](https://github.com/countertek/gatered/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/countertek/gatered/actions/workflows/ci.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n## Todos\n\n- [x] Reddit Gateway API and functions (fetch posts and comments)\n- [x] Add support to fetch past submissions list using pushshift\n- [x] Add GitHub Action CI check and publish flow\n- [x] Publish on PyPI w/ portry\n- [ ] Refine documentation in README and add examples\n- [ ] Prepare test cases\n\n',
    'author': 'Darwin',
    'author_email': 'darekaze@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CounterTek/gatered',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
