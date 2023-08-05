# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src',
 'src.external',
 'src.external.libpgm',
 'src.external.pyBN',
 'src.external.pyBN.classes',
 'src.external.pyBN.classes._tests',
 'src.external.pyBN.classification',
 'src.external.pyBN.inference',
 'src.external.pyBN.inference._tests',
 'src.external.pyBN.inference.map_exact',
 'src.external.pyBN.inference.marginal_approx',
 'src.external.pyBN.inference.marginal_exact',
 'src.external.pyBN.io',
 'src.external.pyBN.io._tests',
 'src.external.pyBN.learning',
 'src.external.pyBN.learning.parameter',
 'src.external.pyBN.learning.parameter._tests',
 'src.external.pyBN.learning.structure',
 'src.external.pyBN.learning.structure._tests',
 'src.external.pyBN.learning.structure.constraint',
 'src.external.pyBN.learning.structure.exact',
 'src.external.pyBN.learning.structure.hybrid',
 'src.external.pyBN.learning.structure.naive',
 'src.external.pyBN.learning.structure.score',
 'src.external.pyBN.learning.structure.tree',
 'src.external.pyBN.plotting',
 'src.external.pyBN.utils',
 'src.external.pyBN.utils._tests',
 'src.preprocess',
 'src.utils']

package_data = \
{'': ['*'], 'src': ['BAMT.egg-info/*', 'data/*', 'img/*']}

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
    'version': '0.1.1',
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
