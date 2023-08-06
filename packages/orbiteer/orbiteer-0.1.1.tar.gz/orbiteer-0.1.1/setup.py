# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orbiteer',
 'orbiteer.inputgenerators',
 'orbiteer.notifiers',
 'orbiteer.optimizers',
 'orbiteer.retries',
 'orbiteer.targets']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'orbiteer',
    'version': '0.1.1',
    'description': 'An optimizing chunking command runner',
    'long_description': '# Orbiteer\n\nA tool to control time-range based scripts, programs, and more.\n\n# Goals\n\n1. Provide a consistent, elegant way of running a script repeatedly with varied inputs in a useful way, such as fitting a goal run-time.\n2. Provide clear error handling and notification, failing gracefully.\n3. Be highly configurable.\n4. Be highly tested.\n\n\n# Wanted Features\n\n#### Legend:\n\n| Symbol | Meaning |\n|--------|---------|\n| :white_check_mark: | Merged |\n| :yellow_square: | In progress |\n| :red_square: | Not yet begun |\n\n### Input Generation:\n- :white_check_mark: Datetime range\n  - :white_check_mark: Old -> New\n  - :white_check_mark: New -> Old\n- :red_square: Iterate over item chunks\n  - :red_square: In presented order\n  - :red_square: Sorted\n\n### Target Measurement\n- :white_check_mark: Direct time taken by command\n- :white_check_mark: Number returned by command\n\n### Optimization Strategy\n- :white_check_mark: Direct ratio\n  - :white_check_mark: With damping\n- :red_square: PID\n\n### Targets\n- :white_check_mark: Run command line\n  - :white_check_mark: Args at end of command string\n  - :red_square: Command line formatting\n- :red_square: Call URL\n  - :red_square: Via request parameters\n  - :red_square: Via request body\n- :red_square: Append to file\n\n### Failure retries\n- :white_check_mark: Quit\n- :red_square: N retries (before quit)\n  - :red_square: Immediately\n  - :red_square: Timed wait\n  - :red_square: Exponential backoff\n- :red_square: Skip\n  - :red_square: Retry pattern and then skip\n  - :red_square: Skip and retry again at end of run\n\n### Notification methods\n- :yellow_square: Logs\n- :red_square: User-named scripts\n- :red_square: [PushOver](https://pushover.net/)\n\n### Notification events\n- :yellow_square: Nominal completion\n- :yellow_square: Erroring out\n- :red_square: N% completion\n- :red_square: Time passed\n\n\n# Development\n\n## Setup\n1. Install [Poetry](https://python-poetry.org/docs/#installation)\n2. Run `./scripts/setup.sh`\n\n## Check lint & formatting\n```\nmake lint\n```\n\n## Fix formatting\n```\nmake format\n```\n\n## Run tests & view coverage\n```\nmake test\n```\n\n## Check lint & run tests\n```\nmake\n```\n',
    'author': 'Avery Fischer',
    'author_email': 'avery@averyjfischer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/biggerfisch/orbiteer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
