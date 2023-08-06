# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['media',
 'tracks',
 'wkz',
 'wkz.best_sections',
 'wkz.device',
 'wkz.gis',
 'wkz.initial_trace_data',
 'wkz.io',
 'wkz.migrations',
 'wkz.plotting',
 'wkz.templatetags',
 'wkz.tools',
 'wkz.tools.migration_utils',
 'workoutizer']

package_data = \
{'': ['*'],
 'wkz': ['static/css/*',
         'static/img/*',
         'static/js/*',
         'static/js/plugins/*',
         'templates/*',
         'templates/activity/*',
         'templates/awards/*',
         'templates/lib/*',
         'templates/map/*',
         'templates/plotting/*',
         'templates/settings/*',
         'templates/sport/*']}

modules = \
['pyproject']
install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'bokeh==1.4.0',
 'channels>=3.0.4,<4.0.0',
 'click>=8.0.4,<9.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'django-colorfield>=0.6.3,<0.7.0',
 'django-eventstream>=4.4.0,<5.0.0',
 'django>=4.0.2,<5.0.0',
 'djangorestframework>=3.13.1,<4.0.0',
 'fitparse>=1.2.0,<2.0.0',
 'geopy>=2.1.0,<3.0.0',
 'gpxpy>=1.5.0,<2.0.0',
 'huey>=2.4.3,<3.0.0',
 'luddite>=1.0.2,<2.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'psutil>=5.9.0,<6.0.0',
 'pyudev>=0.23.2,<0.24.0',
 'sportgems>=0.7.1,<0.8.0',
 'tenacity>=8.0.1,<9.0.0',
 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['wkz = workoutizer.cli:wkz']}

setup_kwargs = {
    'name': 'workoutizer',
    'version': '0.25.0',
    'description': '🏋️ Browser based Sport and Workout Organizer 🏃\u200d♀️',
    'long_description': "# Workoutizer\n\n[![PyPI](https://badge.fury.io/py/workoutizer.svg)](https://badge.fury.io/py/workoutizer)\n[![Python](https://img.shields.io/pypi/pyversions/workoutizer.svg?style=plastic)](https://badge.fury.io/py/workoutizer)\n[![Build Status](https://github.com/fgebhart/workoutizer/actions/workflows/matrix_test.yml/badge.svg)](https://github.com/fgebhart/workoutizer/actions/workflows/matrix_test.yml)\n[![Setup on Raspberry Pi](https://github.com/fgebhart/workoutizer/actions/workflows/raspberry_pi_test.yml/badge.svg)](https://github.com/fgebhart/workoutizer/actions/workflows/raspberry_pi_test.yml)\n[![Coverage Badge](https://raw.githubusercontent.com/fgebhart/workoutizer/master/.github/badges/coverage.svg)](https://raw.githubusercontent.com/fgebhart/workoutizer/master/.github/badges/coverage.svg)\n[![Downloads](https://pepy.tech/badge/workoutizer/month)](https://pepy.tech/project/workoutizer)\n\nWorkoutizer is a simple web application for organizing your workouts and sports activities. It is designed to work\nlocally on any UNIX-like system running Python.\n\nTrack your activities to get an overview of your overall training, similar to platforms like\n[strava](https://www.strava.com/) or [garmin connect](https://connect.garmin.com/) - but without\nuploading all your sensitive health data to some 3rd party cloud.\n\n\n## Features\n\n* Automatic import of Garmin `.fit` files and `.gpx` files\n* Automatic naming of activities based on daytime, sport and geo location\n* Render your activity gps data on different OSM maps\n* Plot your activity specific data e.g. heart rate, pace, temperature, cadence and altitude\n* Integrate laps into both plots and maps\n* Connected plots and map via mouse hovering\n* Find sections with highest speed and max altitude gain using [sportgems](https://github.com/fgebhart/sportgems) and\n  highlight on map\n* Add untracked activities manually via the GUI\n* Export activities as `.gpx` files\n* Add as many different sports as you want\n\n\n## Status\n\nWorkoutizer is still in a somewhat experimental phase. Things might change a lot from one version to another. However,\nI'm happy to receive bug reports and feedback.\n\n\n## Getting Started\n\nInstall workoutizer using pip\n```\npip install workoutizer\n```\n\nInitialize workoutizer to provide some demo data and run it:\n```\nwkz init --demo\nwkz run\n```\n\nSee the help description of the CLI with `wkz --help` and subcommands, e.g.: `wkz manage --help`. \n\nIn case you want to run workoutizer on a Raspberry Pi in your local network, follow the \n[Raspberry Pi setup instructions](https://github.com/fgebhart/workoutizer/tree/main/setup).\n\n\n## Gallery \n\n Dashboard             |  Sport Page\n:-------------------------:|:-------------------------:\n![](https://i.imgur.com/3CUCGC8.png)  |  ![](https://i.imgur.com/p5FcrHz.png)\n\n Activity Page 1/2             |  Activity Page 2/2\n:-------------------------:|:-------------------------:\n![](https://i.imgur.com/FnVFz9P.png)  |  ![](https://i.imgur.com/zp8iQcm.png)\n\n\n## Changelog\n\nSee [Changelog](https://github.com/fgebhart/workoutizer/blob/main/CHANGELOG.md).\n\n\n## Contributing\n\nContributions are welcome - check out the [Contribution Guidelines](https://github.com/fgebhart/workoutizer/blob/main/CONTRIBUTING.md).\n\n\n## Thanks\n\nLibraries and other tools used by Workoutizer:\n* [leaflet-ui](https://github.com/Raruto/leaflet-ui) by [Raruto](https://github.com/Raruto)\n* [django-colorfield](https://github.com/fabiocaccamo/django-colorfield) by [Fabio Caccamo](https://github.com/fabiocaccamo)\n* [python-fitparse](https://github.com/dtcooper/python-fitparse) by [dtcooper](https://github.com/dtcooper)\n* [leaflet-color-markers](https://github.com/pointhi/leaflet-color-markers) by [pointhi](https://github.com/pointhi)\n* [Font Awesome Icons](https://fontawesome.com/)\n* [Paper-Dashboard Pro](https://www.creative-tim.com/product/paper-dashboard-2-pro) by [Creative Tim](https://www.creative-tim.com/)\n",
    'author': 'Fabian Gebhart',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fgebhart/workoutizer',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
