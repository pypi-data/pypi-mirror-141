# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['voltorb_flip']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0', 'rich>=11.2.0,<12.0.0']

entry_points = \
{'console_scripts': ['voltorb-flip = voltorb_flip.__main__:cli']}

setup_kwargs = {
    'name': 'voltorb-flip',
    'version': '1.1.0',
    'description': 'A minigame of the Goldenrod and Celadon Game Corners in the Korean and Western releases of Pokémon HeartGold and SoulSilver.',
    'long_description': '# VoltorbFlip\n\nA minigame of the Goldenrod and Celadon Game Corners in the Korean and Western releases of Pokémon HeartGold and SoulSilver.\n\nA Python engine (and a CLI) for the game of [Voltorb Flip](https://bulbapedia.bulbagarden.net/wiki/Voltorb_Flip).\n\n## Install\n\n```shell\npip install voltorb-flip\n```\n\n## Run\n\n```shell\nvoltorb-flip new\n```\n\n## Play\n\n```text\n   1 2 3 4 5\n a ? ? ? ? ? 3 2\n b ? ? ? ? ? 5 1\n c ? ? ? ? ? 7 0\n d ? ? ? ? ? 6 1\n e ? ? ? ? ? 4 2\n   6 5 5 3 6\n   0 2 0 2 2\n\nInstructions: Flip f<row><column>, Mark m<row><column>, Quit q\nLv. 1 | Score 1 >\n```\n\n(This is how it really looks:)\n\n![Actual screen capture](https://ik.imagekit.io/thatcsharpguy/other_sites/github/Screenshot_2022-03-05_at_12.22.01.png?ik-sdk-version=javascript-1.4.3&updatedAt=1646482970905)\n',
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fferegrino/voltorb-flip',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
