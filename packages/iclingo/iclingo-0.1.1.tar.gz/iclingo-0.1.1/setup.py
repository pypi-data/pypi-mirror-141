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
    'version': '0.1.1',
    'description': '🔴🟢🔵 clingo kernel for Jupyter',
    'long_description': '# iclingo\n\n🔴🟢🔵 [clingo](https://potassco.org/clingo/) kernel for\n[Jupyter](https://jupyter.org/).\n\n## Install\n\nTo install, simply run\n\n`pip install iclingo`\n\n## Usage\n\nOnce installed, you can run clingo code directly in jupyter, alongside typical\njupyter functionality such as markdown cells. An example of this is available in\n[examples/](examples/).\n\n### Limitations\n\n- No syntax highlighting is available\n- Currently, no configuration options cannot be passed to a given cell. This\n  means that the default clingo options are used, such that for a problem with\n  multiple answers, only the first answer is shown.\n- Multi-short solving is not supported\n',
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
