# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wipe_clean']

package_data = \
{'': ['*']}

install_requires = \
['rich>=11.2.0,<12.0.0']

entry_points = \
{'console_scripts': ['wipe-clean = wipe_clean.main:cli']}

setup_kwargs = {
    'name': 'wipe-clean',
    'version': '0.1.3',
    'description': 'Clean your terminal in a ritual way',
    'long_description': '# Wipe Clean\n\n![PyPI](https://img.shields.io/pypi/v/wipe-clean?logo=pypi)\n![PyPI - Status](https://img.shields.io/pypi/status/wipe-clean?logo=pypi)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/wipe-clean?logo=pypi)\n\nClean your terminal in a ritual way. Works on Windows, Linux and macOS.\n\n![demo](https://github.com/wenoptics/python-wipe-clean/blob/master/doc/terminal.gif?raw=true)\n\n\n```bash\npip install wipe-clean\n```\n\n> `wipe-clean` requires Python 3.6.1 and above. Note that Python 3.6.0 is\n not supported due to lack of `NamedTuples` typing.\n\n\n## Usage\n\n```bash\nwipe-clean\n```\n\n\n## Related Projects\n\n- [`JeanJouliaCode/wipeclean`](https://github.com/JeanJouliaCode/wipeClean) (JavaScript)\n\n  The animation part is a direct port of `JeanJouliaCode/wipeclean`.\n',
    'author': 'wenoptk',
    'author_email': 'wenoptics@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wenoptics/python-wipe-clean',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
