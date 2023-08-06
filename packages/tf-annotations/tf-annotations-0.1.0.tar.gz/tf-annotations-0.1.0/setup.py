# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tf_annotations']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['tf-annotations = tf_annotations.cmd:cli']}

setup_kwargs = {
    'name': 'tf-annotations',
    'version': '0.1.0',
    'description': 'Tool to report on annotations such as TODO',
    'long_description': None,
    'author': 'Russell Whelan',
    'author_email': 'russell.whelan+python@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
