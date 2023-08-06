# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nbed', 'nbed.localizers', 'nbed.scf']

package_data = \
{'': ['*']}

install_requires = \
['PennyLane-Qchem>=0.17.0,<0.18.0',
 'PennyLane>=0.17.0,<0.18.0',
 'PyYAML>=5.4.1,<6.0.0',
 'cached-property>=1.5.2,<2.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'nbsphinx>=0.8.8,<0.9.0',
 'openfermion<1.1.0',
 'pandoc>=2.1,<3.0',
 'py3Dmol>=1.7.0,<2.0.0',
 'pyscf==1.7.6',
 'qiskit-nature>=0.2.2,<0.3.0',
 'types-PyYAML>=5.4.11,<6.0.0']

entry_points = \
{'console_scripts': ['nbed = nbed.embed:cli']}

setup_kwargs = {
    'name': 'nbed',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Michael Williams',
    'author_email': 'michael.williams.20@ucl.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
