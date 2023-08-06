# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyametista',
 'pyametista.adapters',
 'pyametista.engine',
 'pyametista.engine.bands',
 'pyametista.engine.components',
 'pyametista.exports']

package_data = \
{'': ['*']}

install_requires = \
['mysql-connector-python>=8.0.28,<9.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'reportlab>=3.6.8,<4.0.0']

setup_kwargs = {
    'name': 'pyametista',
    'version': '0.1.2',
    'description': 'Módulo Python para geração de PDF utilizando arquivos .jrxml (JasperReports)',
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
