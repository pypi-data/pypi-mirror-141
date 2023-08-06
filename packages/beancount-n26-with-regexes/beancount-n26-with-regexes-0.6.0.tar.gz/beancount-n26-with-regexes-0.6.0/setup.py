# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_n26_with_regexes']

package_data = \
{'': ['*']}

install_requires = \
['beancount>=2.2,<3.0']

setup_kwargs = {
    'name': 'beancount-n26-with-regexes',
    'version': '0.6.0',
    'description': 'Beancount Importer for N26 CSV exports with extended regex classification',
    'long_description': '# Beancount N26 Importer\n\n[![image](https://github.com/Eazhi/beancount-n26-with-regexes/workflows/beancount-n26/badge.svg)](https://github.com/Eazhi/beancount-n26-with-regexes/workflows/beancount-n26/badge.svg)\n\n[![image](https://img.shields.io/pypi/v/beancount-n26.svg)](https://pypi.python.org/pypi/beancount-n26)\n\n[![image](https://img.shields.io/pypi/pyversions/beancount-n26.svg)](https://pypi.python.org/pypi/beancount-n26)\n\n[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n`beancount-n26-with-regexes` provides a [Beancount] Importer for converting CSV exports of\n[N26] account summaries to the Beancount format.\n\n## Installation\n\n```sh\n$ pip install beancount-n26\n```\n\nIn case you prefer installing from the Github repository, please note that\n`main` is the development branch so `stable` is what you should be installing\nfrom.\n\n## Usage\n\n```python\nfrom beancount_n26_with_regexes import N26Importer\n\nCONFIG = [\n    N26Importer(\n        IBAN_NUMBER,\n        \'Assets:N26\',\n        language=\'en\',\n        file_encoding=\'utf-8\',\n        fill_default=True,\n        account_to_ayees={\n           "Expenses:Food:Restaurants": [\n              # Regex \'style\' payee name\n              "amorino",\n              "five guys.*",\n           ]\n        }\n    ),\n]\n```\n\n## References\n\nThis is a fork of: https://github.com/siddhantgoel/beancount-n26\n\n[Beancount]: http://furius.ca/beancount/\n[N26]: https://n26.com/\n[Poetry]: https://poetry.eustace.io/\n',
    'author': 'KHUAT DUY Paul',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Eazhi/beancount-n26-with-regexes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
