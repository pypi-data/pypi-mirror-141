# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynfsesp', 'pynfsesp.gateways', 'pynfsesp.utils']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.8.0,<5.0.0',
 'pycrypto>=2.6.1,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'rsa>=4.8,<5.0',
 'urllib3>=1.26.8,<2.0.0']

setup_kwargs = {
    'name': 'pynfsesp',
    'version': '0.1.0',
    'description': 'Módulo para emissão de Notas Fiscais de Serviço para a Prefeitura de SP',
    'long_description': None,
    'author': 'Bruno Souza',
    'author_email': 'bruno@komu.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
