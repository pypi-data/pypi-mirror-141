# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vega', 'vega.data', 'vega.vega_count']

package_data = \
{'': ['*']}

install_requires = \
['adjustText>=0.7.3,<0.8.0',
 'anndata>=0.7.5,<0.8.0',
 'markdown==3.3.4',
 'matplotlib>=3.1.3,<4.0.0',
 'numpy>=1.18.1,<2.0.0',
 'pandas>=1.0.1,<2.0.0',
 'scanpy>=1.7.0,<2.0.0',
 'scikit-learn>=0.23.1,<0.24.0',
 'scipy>=1.6.0,<2.0.0',
 'scvi-tools==0.9.0',
 'seaborn>=0.10.0,<0.11.0',
 'setuptools<=59.5.0',
 'torch>=1.8.0,<2.0.0',
 'tqdm>=4.56.0,<5.0.0']

extras_require = \
{'docs': ['furo>=2022.3.4,<2023.0.0',
          'sphinx>=4.1,<4.4',
          'sphinx-autodoc-typehints',
          'sphinx-design',
          'sphinx-gallery>0.6',
          'sphinx_copybutton<=0.3.1',
          'sphinx_remove_toctrees',
          'sphinxext-opengraph'],
 'docs:python_version < "3.8"': ['typing_extensions']}

setup_kwargs = {
    'name': 'scvega',
    'version': '0.0.2',
    'description': 'VEGA: a VAE Enhanced by Gene Annotations for interpretable scRNA-seq deep learning',
    'long_description': None,
    'author': 'Lucas Seninge',
    'author_email': 'lseninge@ucsc.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LucasESBS/vega',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
