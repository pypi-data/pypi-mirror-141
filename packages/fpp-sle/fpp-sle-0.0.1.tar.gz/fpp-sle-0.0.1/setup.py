# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fpp_sle', 'fpp_sle.fpp', 'fpp_sle.sde', 'fpp_sle.sle']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.55.1,<0.56.0', 'numpy>=1.18,<1.22']

setup_kwargs = {
    'name': 'fpp-sle',
    'version': '0.0.1',
    'description': 'Implements FPP and SLE algorithms',
    'long_description': '# fpp-sle\n\n> Implements FPP and SLE algorithms\n\n## Usage\n\nCurrently only available in development mode. To install the full development version,\nuse:\n\n```sh\ngit clone https://github.com/engeir/fpp-sle\ncd fpp-sle\npoetry install\npre-commit install\n```\n\nIf you are only interested in using the project, you can install it into your virtual\nenvironment with:\n\n```sh\ngit clone https://github.com/engeir/fpp-sle\ncd fpp-sle\npoetry install --no-dev\n```\n',
    'author': 'engeir',
    'author_email': 'eirroleng@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
