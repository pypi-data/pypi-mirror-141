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
    'version': '0.1.2',
    'description': 'Tools for publishing albums to the web and digital stores',
    'long_description': '# pyBlamscamp\n\n![CC0 license badge](https://licensebuttons.net/p/zero/1.0/88x31.png)\n\nThis is based on [blamscamp](https://github.com/blackle/blamscamp), with an intention towards being a standalone program you run on your computer to automatically encode an album of songs into a bunch of different formats for distribution on various platforms, such as [itch.io](https://itch.io/), or for hosting on your own website.\n\nTo use it, you\'ll need to install LAME, oggenc, and FLAC; on macOS you can install these via [homebrew](https://brew.sh/), on Linux you can use your system\'s package manager, and on Windows you\'re on your own.\n\nYou\'ll also need to install [Python](https://python.org), after which you can install pyBlamscamp with:\n\n```\npip install blamscamp\n```\n\n`blamscamp --help` should guide you the rest of the way there.\n\n## Building an album\n\nMake a directory with all of your source audio files and artwork and so on. Create a JSON file named `album.json` (which can be overridden) that looks something like this:\n\n```json\n{\n    "artist": "The artist of the album",\n    "title": "The title of the album",\n    "bg_color": "black",\n    "fg_color": "white",\n    "highlight_color": "#cc00ff",\n    "artwork": "album_cover.jpg",\n    "tracks": [{\n        "filename": "the first track.wav",\n        "title": "The First Track",\n        "artwork": "track1_cover.jpg",\n        "lyrics": ["This is the first line",\n            "This is the second line",\n            "This is the third line",\n            "",\n            "This is the second verse",\n            "This song just keeps getting worse"],\n        "hidden": false,\n        "preview": true\n    }]\n}\n```\n\nBasically, the top-level album contains the following properties (all optional):\n\n* `artist`: The artist for the album as a whole\n* `title`: The album\'s title\n* `bg_color`, `fg_color`, `highlight_color`: The color theme for the player\n* `artwork`: an image file to use for the album\'s cover art\n* `tracks`: an array of track descriptions, in album order\n\nEach track element contains:\n\n* `title`: The title of the track\n* `artist`: The artist of this track, if different from the album as a whole\n* `artwork`: Track-specific cover art (e.g. for a single)\n* `lyrics`: An array of strings, one line of lyrics per string; alternately, this can be the name of a text file to read the lyrics from\n* `hidden`: A boolean for whether to hide this track from the web player entirely (e.g. a purchase bonus); defaults to `false`\n* `preview`: A boolen for whether to generate a preview for the web player; defaults to `true`\n\nSee the [sample album JSON file](https://github.com/fluffy-critter/pyBlamscamp/blob/main/test_album/album.json) for a rough example.\n\n## Contributing\n\nPull requests are welcome! But please note the following:\n\nThe generated blamscamp player must not receive any added dependencies. The generator must stay as a single, self-contained file that is as small as reasonably possible. The point is for the generated file to be lightweight. Stick to Vanilla JS.\n\n## License\n\nThis software is public domain.\n',
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
