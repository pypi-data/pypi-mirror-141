# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nba_stats_tracking',
 'nba_stats_tracking.models',
 'nba_stats_tracking.models.boxscore',
 'nba_stats_tracking.models.matchups',
 'nba_stats_tracking.models.scoreboard',
 'nba_stats_tracking.models.tracking',
 'nba_stats_tracking.models.tracking_shots']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'nba-stats-tracking',
    'version': '1.0.7',
    'description': 'A package to work with NBA player tracking stats using the NBA Stats API',
    'long_description': None,
    'author': 'dblackrun',
    'author_email': 'darryl.blackport@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
