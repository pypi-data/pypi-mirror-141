# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blamscamp']

package_data = \
{'': ['*'], 'blamscamp': ['jinja_templates/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'Pillow>=9.0.1,<10.0.0',
 'awesome-slugify>=1.6.5,<2.0.0',
 'mutagen>=1.45.1,<2.0.0']

entry_points = \
{'console_scripts': ['blamscamp = blamscamp.__init__:main']}

setup_kwargs = {
    'name': 'blamscamp',
    'version': '0.1.0',
    'description': 'Tools for publishing albums to the web and digital stores',
    'long_description': "# pyBlamscamp\n\n![CC0 license badge](https://licensebuttons.net/p/zero/1.0/88x31.png)\n\nThis is based on [blamscamp](https://github.com/blackle/blamscamp), with an intention towards being a standalone program you run on your computer to automatically encode an album of songs into a bunch of different formats for distribution on various platforms, such as [itch.io](https://itch.io/), or for hosting on your own website.\n\nTo use it, you'll need to install LAME, oggenc, and FLAC; on macOS you can install these via [homebrew](https://brew.sh/), on Linux you can use your system's package manager, and on Windows you're on your own.\n\nYou'll also need to install [Python](https://python.org), after which you can install pyBlamscamp with:\n\n```\npip install pyBlamscamp\n```\n\n`blamscamp --help` should guide you the rest of the way there.\n\nSee the [sample album JSON file](test_album/album.json) for a rough example of how to format the album spec file. Supported attributes are (currently):\n\n* `artist`: The name of the artist (can be overriddedn per-track)\n* `title`: The title of the album or track\n* `year`: The release year\n* `lyrics`: The lyrics of the track, in the form of an array of lines\n* `hidden`: Whether a track should be hidden from the web player entirely (default: `false`)\n* `preview`: Whether a track should be played in the player (default: `true`)\n\n## Contributing\n\nPull requests are welcome! But please note the following:\n\nThe generated blamscamp player must not receive any added dependencies. The generator must stay as a single, self-contained file that is as small as reasonably possible. The point is for the generated file to be lightweight. Stick to Vanilla JS.\n\n## License\n\nThis software is public domain.\n",
    'author': 'fluffy',
    'author_email': 'fluffy@beesbuzz.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
