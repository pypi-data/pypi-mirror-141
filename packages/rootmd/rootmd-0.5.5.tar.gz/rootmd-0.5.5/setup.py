# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rootmd']

package_data = \
{'': ['*'],
 'rootmd': ['data/*', 'data/css/*', 'data/css/prismjs/*', 'data/js/*']}

install_requires = \
['mistletoe>=0.8.1,<0.9.0',
 'pygments>=2.11.2,<3.0.0',
 'pyyaml>=5.4.1,<6.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=11.0.0,<12.0.0',
 'watchdog>=2.1.6,<3.0.0']

setup_kwargs = {
    'name': 'rootmd',
    'version': '0.5.5',
    'description': 'RootMD is a markdown processor for markdown with ROOT-flavored c++ code. RootMD can execute c++ code and inject the output (from stdout, stderr) and link or embed image outputs',
    'long_description': None,
    'author': 'Daniel Brandenburg',
    'author_email': 'hello@jdbburg.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
