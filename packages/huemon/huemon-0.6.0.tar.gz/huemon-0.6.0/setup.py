# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['huemon',
 'huemon.api',
 'huemon.commands',
 'huemon.commands_available',
 'huemon.commands_internal',
 'huemon.discoveries',
 'huemon.discoveries_available',
 'huemon.infrastructure']

package_data = \
{'': ['*'], 'huemon': ['commands_enabled/*', 'discoveries_enabled/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'coverage[toml]>=6.3.2,<7.0.0',
 'mypy>=0.931,<0.932',
 'nox>=2022.1.7,<2023.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'types-PyYAML>=6.0.4,<7.0.0']

setup_kwargs = {
    'name': 'huemon',
    'version': '0.6.0',
    'description': 'Monitor your Philips Hue network',
    'long_description': '# Huemon\n\n[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)\n[![Build](https://github.com/edeckers/huemon/actions/workflows/test.yml/badge.svg)](https://github.com/edeckers/huemon/actions/workflows/test.yml)\n[![PyPI](https://img.shields.io/pypi/v/huemon.svg?maxAge=3600)](https://pypi.org/project/huemon)\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n\nZabbix monitoring with low-level discovery for Philips Hue networks.\n\n![Dashboard: sensors](https://raw.githubusercontent.com/edeckers/huemon/develop/docs/assets/dashboard-sensors.png?raw=true "Dashboard: sensors")\n\n## Requirements\n\n- Zabbix server 5.0+\n- Zabbix agent 5.0+\n- Python 3.7+ on Zabbix agent machine\n\n## Installation\n\n```bash\npip3 install huemon\n```\n\n## Configuration\n\n1. Copy `config.example.yml` from `src/huemon` to `/path/to/config.yml`\n2. Make necessary changes\n3. Provide the path through environment variable `HUEMON_CONFIG_PATH`\n\n### Enabling commands and discoveries\n\n#### Automatically\n\n```bash\nHUEMON_CONFIG_PATH=/path/to/config.yml python3 -m huemon install_available commands\nHUEMON_CONFIG_PATH=/path/to/config.yml python3 -m huemon install_available discoveries\n```\n\n#### Manually\n\n```bash\nln -s /path/to/commands_available/command_name.py /path/to/commands_enabled/command_name.py\nln -s /path/to/discoveries_available/command_name.py /path/to/discoveries_enabled/command_name.py\n```\n\n## Usage\n\n### Shell\n\n```bash\nHUEMON_CONFIG_PATH=/usr/bin/python3 -m huemon discover lights\n```\n\n### Docker\n\n```bash\ndocker run -v /path/to/huemon/config:/etc/huemon huemon:0.1.0 discover lights\n```\n\n### Zabbix agent configuration\n\n```\n# file:/path/to/zabbix/agent/conf.d/hue.conf\n\nUserParameter=hue.discovery[*],HUEMON_CONFIG_PATH=/path/to/config.yml /usr/bin/python3 -m huemon discover $1\nUserParameter=hue.value[*],HUEMON_CONFIG_PATH=/path/to/config.yml /usr/bin/python3 -m huemon $1 $2 $3\n```\n\n## Screenshots\n\n### Dashboards\n![Dashboard: sensors](https://raw.githubusercontent.com/edeckers/huemon/develop/docs/assets/dashboard-sensors.png?raw=true "Dashboard: sensors")\n\n### Discoveries\n\n![Discoveries: batteries](https://raw.githubusercontent.com/edeckers/huemon/develop/docs/assets/discoveries-batteries.png?raw=true "Discoveries: batteries")\n\n![Discoveries: lights](https://raw.githubusercontent.com/edeckers/huemon/develop/docs/assets/discoveries-lights.png?raw=true "Discoveries: lights")\n\n![Discoveries: sensors](https://raw.githubusercontent.com/edeckers/huemon/develop/docs/assets/discoveries-sensors.png?raw=true "Discoveries: sensors")\n\n### Template\n\n![Template](https://raw.githubusercontent.com/edeckers/huemon/develop/docs/assets/template-discoveries.png?raw=true "Template")\n\n\n## License\n\nMPL-2.0\n',
    'author': 'Ely Deckers',
    'author_email': None,
    'maintainer': 'Ely Deckers',
    'maintainer_email': None,
    'url': 'https://github.com/edeckers/huemon.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
