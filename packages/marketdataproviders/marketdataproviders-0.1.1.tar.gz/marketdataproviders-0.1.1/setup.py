# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['marketdataproviders']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.2,<2.0.0', 'pandas>=1.4.1,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'marketdataproviders',
    'version': '0.1.1',
    'description': 'APIs around Market Data Providers',
    'long_description': "# Market Data Providers\n\nMiscellaneous APIs around Market Data providers.\n\n## APIs\n\nCurrently only basic access to: <https://eodhistoricaldata.com/> is implemented.\n\n\n## Build\n\nThis is built using [Poetry](https://python-poetry.org/).\n\n```bash\n# after checkout, within top-level checkout directory\npoetry install\n\n# To update dependencies, or after `poetry add ...`\npoetry update\n\n# to make sure we are using our virtual env's tooling (created\n# automatically by poetry, much like conda env)\n# We can, for example add ipython as a dev dependency, then shell into our\n# env, only then will we get this install. Use `which ipython` to verify.\npoetry shell\n\n# To build distributable packages\npoetry build\n```\n\n## Publishing\n\n### To PyPi\n\nCreate PyPI account with a new token.\n\nAdd this to poetry's config:\n\n```\npoetry config pypi-token.pypi <my-token>\n```\n\nSimply publish:\n\n```\npoetry publish\n```\n\n\n### To Local Repository\n\nOnce off only: Prepare Local Repository\n\nSee: \n\n* https://pypi.org/project/pypiserver/: Install this.\n* https://python-poetry.org/docs/master/repositories/\n\n\n```bash\n# Create location\nLOCAL_REPO_FS=$HOME/.local/home-pypi\nmkdir -p $LOCAL_REPO_FS\ncd $LOCAL_REPO_FS\n\n# Run pypi-server in local repo fs, unauthorised mode.\npypi-server -i 127.0.0.1 -v -P . -a . -p 9292 .\n```\nAdd repository name to `poetry` config:\n\n```bash\npoetry config repositories.home-pypi http://localhost:9292/\n```\nUpdate `pip` configuration to use this extra index.\n\n```\n# ~/.pip/pip.conf -> https://pypi.org/project/pypiserver/#configuring-pip\n# Add the following config\n\n[global]\nextra-index-url = http://localhost:9292/simple/\n```\n\nTo publish to local repo:\n\n```\n# Publish distributable packages to local repo set-up with name above.\n# Just press Enter when username asked, we don't have authentication on.\npoetry publish --repository home-pypi\n```",
    'author': 'Kamal Advani',
    'author_email': 'kamal.advani@namingcrisis.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
