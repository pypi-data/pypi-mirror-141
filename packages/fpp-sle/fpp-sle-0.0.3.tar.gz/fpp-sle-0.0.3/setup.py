# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fpp_sle', 'fpp_sle.fpp', 'fpp_sle.sde']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.55.1,<0.56.0', 'numpy>=1.18,<1.22', 'superposed-pulses>=1.2,<2.0']

setup_kwargs = {
    'name': 'fpp-sle',
    'version': '0.0.3',
    'description': 'Implements FPP and SLE algorithms',
    'long_description': '# fpp-sle\n\n[![codecov](https://codecov.io/gh/engeir/fpp-sle/branch/main/graph/badge.svg?token=8I5VE7LYA4)](https://codecov.io/gh/engeir/fpp-sle)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n> Implements FPP and SLE algorithms\n\n## Usage\n\nCurrently only available in development mode. To install the full development version,\nuse:\n\n```sh\ngit clone https://github.com/engeir/fpp-sle\ncd fpp-sle\npoetry install\npre-commit install\n```\n\nIf you are only interested in using the project, you can install it into your virtual\nenvironment with:\n\n```sh\ngit clone https://github.com/engeir/fpp-sle\ncd fpp-sle\npoetry install --no-dev\n```\n',
    'author': 'engeir',
    'author_email': 'eirroleng@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
