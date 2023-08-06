# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skqulacs', 'skqulacs.circuit', 'skqulacs.qnn', 'skqulacs.qsvm']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.4,<2.0.0',
 'qulacs-osaka>=0.2.0,<0.3.0',
 'scikit-learn>=1.0.1,<2.0.0',
 'scipy>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'skqulacs',
    'version': '0.1.0',
    'description': 'scikit-qulacs is a library for quantum neural network. This library is based on qulacs and named after scikit-learn.',
    'long_description': '\n# scikit-qulacs\n\n[scikit-qulacsチュートリアル](https://github.com/Qulacs-Osaka/scikit-qulacs/blob/main/doc/source/notebooks/0_tutorial.ipynb)\n\n',
    'author': 'Qulacs-Osaka',
    'author_email': 'qulacs.osaka@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Qulacs-Osaka/scikit-qulacs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
