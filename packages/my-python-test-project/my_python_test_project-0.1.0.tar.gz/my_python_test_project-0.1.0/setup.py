# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['my_python_test_project']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.1.0,<23.0.0',
 'click>=8.0.4,<9.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'flake8>=4.0.1,<5.0.0',
 'marshmallow>=3.14.1,<4.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['my-python-test-project = '
                     'my_python_test_project.console:main']}

setup_kwargs = {
    'name': 'my-python-test-project',
    'version': '0.1.0',
    'description': 'This is a test project',
    'long_description': '[![Tests](https://github.com/ossScharom/my-python-test-project/workflows/Tests/badge.svg)](https://github.com/ossScharom/my-python-test-project/actions?workflow=Tests)\n[![Coverage](https://codecov.io/gh/ossScharom/my-python-test-project/branch/master/graph/badge.svg)](https://codecov.io/gh/ossScharom/my-python-test-project)\n',
    'author': 'Jerome Würf',
    'author_email': 'oss@scharom.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ossScharom/my-python-test-project',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
