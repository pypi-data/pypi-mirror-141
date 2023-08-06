# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['article_playground',
 'article_playground.notion',
 'article_playground.notion.endpoints']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0',
 'key>=0.4,<0.5',
 'mypy>=0.931,<0.932',
 'pydantic>=1.9.0,<2.0.0',
 'pytest>=6.2.5,<7.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['noticle = article_playground.__main__:main']}

setup_kwargs = {
    'name': 'article-playground',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'socar-grab',
    'author_email': 'grab@socar.kr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
