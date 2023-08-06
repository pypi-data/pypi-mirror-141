# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iclingo']

package_data = \
{'': ['*']}

install_requires = \
['clingo>=5.5.1,<6.0.0',
 'ipykernel>=6.9.1,<7.0.0',
 'single-source>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'iclingo',
    'version': '0.1.7',
    'description': '🔴🟢🔵 clingo kernel for Jupyter',
    'long_description': '# iclingo\n\n![Compatible python versions](https://img.shields.io/pypi/pyversions/iclingo)\n![build workflow\nbadge](https://img.shields.io/github/workflow/status/thesofakillers/iclingo/build)\n![PyPI version](https://badge.fury.io/py/iclingo.svg)\n\n🔴🟢🔵 [clingo](https://potassco.org/clingo/) kernel for\n[Jupyter](https://jupyter.org/).\n\n## Install\n\nTo install, simply run\n\n```console\npip install iclingo\npython -m iclingo.install\n```\n\n## Usage\n\nOnce installed, you can run clingo code directly in jupyter, alongside typical\njupyter functionality such as markdown cells. An example of this is available in\n[examples/](examples/).\n\n### Limitations\n\n- No syntax highlighting is available\n- Currently, no configuration options can be passed to a given cell. This means\n  that the default clingo options are used, such that for a problem with\n  multiple answers, only the first answer is shown.\n- Multi-shot solving is not supported\n\n## Development\n\nThis repository is mostly based on the documentation presented in\n[_Making simple Python wrapper kernels_](https://jupyter-client.readthedocs.io/en/stable/wrapperkernels.html).\n\nWe use [poetry](https://python-poetry.org/) to track dependencies and build our\npackage.\n\n[GitHub Actions](https://github.com/features/actions) are then used for\nautomatic publishing to [PyPi](https://pypi.org/) upon pushes of\n[git tags](https://git-scm.com/book/en/v2/Git-Basics-Tagging) to the repository.\n\nWhen ready to publish the latest commit, simply run the following:\n\n```console\ngit tag $(poetry version --short)\ngit push --tags\n```\n\nPull requests and contributions are more than welcome. Please refer to the\n[relevant page](https://github.com/thesofakillers/iclingo/contribute).\n',
    'author': 'Giulio Starace',
    'author_email': 'giulio.starace@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thesofakillers/iclingo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
