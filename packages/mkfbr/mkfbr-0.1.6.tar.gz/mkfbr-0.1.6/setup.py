# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkfbr']

package_data = \
{'': ['*'], 'mkfbr': ['database/*', 'json/*']}

setup_kwargs = {
    'name': 'mkfbr',
    'version': '0.1.6',
    'description': 'This simple project only serves as an object of study and/or software testing, do not use it for fraudulent activities.',
    'long_description': "\n# What is make_a_fake_brazilian A.K.A mkfbr? Where is he going? Where does he come from? What does it feed on?\n\n  \nWell, this simple project was born out of a particular need in personal projects. Specifically I needed some information from Brazilians, such as: Name, Address, CPF, CPNJ, Age, among other things. Since then, I decided to make my job easier with a quick and simple to use module.\n\n**Note:** This project only serves as an object of study and/or software testing, do not use it for fraudulent activities.\n\n## Quick note about missing states in the database\n\nThe database for this project was built based on data provided by [CEP ABERTO](https://www.cepaberto.com/), which in turn did not include (when >darkmathew< performed the scraping) the following states: **Maranhão, Rio de Janeiro, Rio Grande do Norte, Roraima and Tocantins**. I apologize to you if you need data generated from any of these regions of Brazil. If you get this information and want to share it with the project, please submit a properly tested and verified PR that includes cities and zip codes for those states.\n\n\n## Install from PyPi\n\n`pip install mkfbr`\n\n  \n## Simple Usage\n\n```python\n\nfrom mkfbr import Make_A_Fake_Brazilian\n\nmkfbr = Make_A_Fake_Brazilian()\n\nbrazilian = mkfbr.get_brazilian()\n\nprint(brazilian)\n\n```\n\nOutput example:\n\n```\n\n{\n    'name': 'Egídia Angelles',\n    'age': 47,\n    'birthday': '26/11/1975',\n    'cpf': '80051493608',\n    'rg': '136076262',\n    'cnpj': '',\n    'address': 'Rua Expedito Pereira de Souza 971',\n    'state': 'Acre',\n    'state_abbreviation': 'AC',\n    'city': 'Bujari',\n    'bairro': 'Centro',\n    'logradouro': ''\n}\n\n```\n\n## Generate Female Person\n\n```python\n\nfrom mkfbr import Make_A_Fake_Brazilian\n\n  \nmkfbr = Make_A_Fake_Brazilian(\n\n    gender_name='F',\n\n)\n\nbrazilian = mkfbr.get_brazilian()\n\n  \nprint(brazilian)\n\n```\n\n\n## Generate Male Person\n\n```python\n\nfrom mkfbr import Make_A_Fake_Brazilian\n\n\nmkfbr = Make_A_Fake_Brazilian(\n\n    gender_name='M',\n\n)\n\nbrazilian = mkfbr.get_brazilian()\n\n  \nprint(brazilian)\n\n```\n\n  \n## Generate CPNJ / RG / CPF with pontuation\n\n\n**Note:** To generate CNPJ the `gen_cnpj` argument needs to be true.\n\n\n```python\n\nfrom mkfbr import Make_A_Fake_Brazilian\n\n  \n\nmkfbr = Make_A_Fake_Brazilian(\n\n    cpf_mode='points',\n\n    rg_mode='points',\n\n    gen_cnpj=True,\n\n    cnpj_mode='points',\n\n)\n\nbrazilian = mkfbr.get_brazilian()\n\nprint(brazilian)\n\n```\n\n  \n\nOutput example:\n\n```\n\n{\n    'name': 'Eros de Assuncao',\n\n    'age': 66,\n\n    'birthday': '15/01/1956',\n\n    'cpf': '058.592.229-20',\n\n    'rg': '57.137.420-4',\n\n    'cnpj': '60.294.437/0001-07',\n\n    'address': 'Avenida André Pereira Lobato, s/n',\n\n    'state': 'Piauí',\n\n    'state_abbreviation': 'PI',\n\n    'city': 'Sebastião Barros',\n\n    'bairro': 'Centro',\n\n    'logradouro': ''\n\n}\n\n```\n",
    'author': 'Matheus Santos',
    'author_email': '78329418+darkmathew@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/darkmathew/make_a_fake_brazilian',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
