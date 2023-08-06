# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['einop']

package_data = \
{'': ['*']}

install_requires = \
['einops>=0.4.0']

setup_kwargs = {
    'name': 'einop',
    'version': '0.0.1',
    'description': '',
    'long_description': '# Einop\n\n_One op to rule them all_\n\nEinop is a very thin wrapper around [einops](https://github.com/arogozhnikov/einops) that combines `rearrange`, `reduce`, and `repeat` into a single `einop` function. This library is a port of [arogozhnikov/einops#91](https://github.com/arogozhnikov/einops/pull/91) by [Miles Cranmer](https://github.com/MilesCranmer) into a separate library, if at some point that PR is merged use `einop` directly from einops instead.\n\n## Installation\n```\npip install einop\n```\n## Usage\n```python\nimport numpy as np\nfrom einop import einop\n\nx = np.random.uniform(size=(10, 20))\ny = einop(x, "height width -> batch width height", batch=32)\n\nassert y.shape == (32, 20, 10)\n```\n\n#### Rearrange\n```python\neinop(x, \'i j k -> k i j\').shape\n>>> (3, 100, 5)\n```\n\n#### Reduction\n```python\nimport numpy as np\nfrom einops import einop\n\nx = np.random.randn(100, 5, 3)\n\neinop(x, \'i j k -> i j\', reduction=\'sum\').shape\n>>> (100, 5)\n```\n\n#### Repeat\n```python\neinop(x, \'i j k -> i j k l\', l=10).shape\n(100, 5, 3, 10)\n```\n',
    'author': 'Cristian Garcia',
    'author_email': 'cgarcia.e88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cgarciae.github.io/einop',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
