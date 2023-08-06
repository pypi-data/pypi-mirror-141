# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphene_protector', 'graphene_protector.django']

package_data = \
{'': ['*']}

install_requires = \
['graphql-core>=2']

extras_require = \
{'optional': ['graphene>=2',
              'graphene-django',
              'strawberry-graphql-django',
              'strawberry-graphql']}

setup_kwargs = {
    'name': 'graphene-protector',
    'version': '0.6.3',
    'description': 'Protects graphene, graphql or strawberry against malicious queries',
    'long_description': None,
    'author': 'alex',
    'author_email': 'devkral@web.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/devkral/graphene-protector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
