# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bamt',
 'bamt.external',
 'bamt.external.libpgm',
 'bamt.external.pyBN',
 'bamt.external.pyBN.classes',
 'bamt.external.pyBN.classes._tests',
 'bamt.external.pyBN.classification',
 'bamt.external.pyBN.inference',
 'bamt.external.pyBN.inference._tests',
 'bamt.external.pyBN.inference.map_exact',
 'bamt.external.pyBN.inference.marginal_approx',
 'bamt.external.pyBN.inference.marginal_exact',
 'bamt.external.pyBN.io',
 'bamt.external.pyBN.io._tests',
 'bamt.external.pyBN.learning',
 'bamt.external.pyBN.learning.parameter',
 'bamt.external.pyBN.learning.parameter._tests',
 'bamt.external.pyBN.learning.structure',
 'bamt.external.pyBN.learning.structure._tests',
 'bamt.external.pyBN.learning.structure.constraint',
 'bamt.external.pyBN.learning.structure.exact',
 'bamt.external.pyBN.learning.structure.hybrid',
 'bamt.external.pyBN.learning.structure.naive',
 'bamt.external.pyBN.learning.structure.score',
 'bamt.external.pyBN.learning.structure.tree',
 'bamt.external.pyBN.plotting',
 'bamt.external.pyBN.utils',
 'bamt.external.pyBN.utils._tests',
 'bamt.preprocess',
 'bamt.utils']

package_data = \
{'': ['*']}

install_requires = \
['gmr==1.6.2',
 'matplotlib==3.5.1',
 'missingno>=0.5.1,<0.6.0',
 'numpy==1.22.2',
 'pandas==1.4.0',
 'pomegranate==0.14.8',
 'pyvis>=0.1.9,<0.2.0',
 'scikit-learn==1.0.2',
 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'bamt',
    'version': '0.1.202',
    'description': 'data modeling and analysis tool based on Bayesian networks',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
