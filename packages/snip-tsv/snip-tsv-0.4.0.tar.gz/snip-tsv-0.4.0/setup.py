# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['snip_tsv']
install_requires = \
['matplotlib>=3.5.1,<4.0.0']

entry_points = \
{'console_scripts': ['snip = snip_tsv:main']}

setup_kwargs = {
    'name': 'snip-tsv',
    'version': '0.4.0',
    'description': 'Crop tabular data files',
    'long_description': "# snip-tsv\n\nCrop tabular data files\n\n## Installation\n\n```bash\npip install snip-tsv\n```\n\n## Usage\n\n```text\n$ snip -h\nusage: snip [-h] [-v] [-H] [-d DELIMITER] [-x PLOT_X] [-y PLOT_Y]\n            [-c CROP_COL] [-s CROP_START] [-e CROP_END]\n            [-o OUT_FILE]\n            in_file\n\npositional arguments:\n  in_file               Input data file. (default: -)\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -v, --version         show program's version number and exit\n  -H, --header          When set assume the first row to be a\n                        header row. By default, no header row is\n                        assumed.\n  -d DELIMITER, --delimiter DELIMITER\n                        The delimiter used in the input data file.\n                        (default: '\\t')\n  -x PLOT_X, --plot-x PLOT_X\n                        Column to use on the x-axis. A 0-indexed\n                        integer or a column heading string.\n                        (default: 0)\n  -y PLOT_Y, --plot-y PLOT_Y\n                        Column to use on the y-axis. A 0-indexed\n                        integer or a column heading string.\n                        (default: 1)\n  -c CROP_COL, --crop-col CROP_COL\n                        Column to search in for --crop-\n                        start/--crop-end values. A 0-indexed\n                        integer or a column heading string.\n                        (default: 0)\n  -s CROP_START, --crop-start CROP_START\n                        Start value to use for cropping\n                        (inclusive). If the column is numeric then\n                        the row with column entry closest to the\n                        given value is used.\n  -e CROP_END, --crop-end CROP_END\n                        End value to use for cropping (exclusive).\n                        If the column is numeric then the row with\n                        column entry closest to the given value is\n                        used. To specify a numeric value relative\n                        to --crop-start use the syntax ':<number>'.\n                        Omit this flag to crop from --crop-start to\n                        the end of the file.\n  -o OUT_FILE, --out-file OUT_FILE\n                        File to write the results to (either an\n                        image or TSV file. If not provided a\n                        matplotlib plot is shown when plotting, and\n                        data is written to stdout when cropping.\n                        (default: -)\n```\n",
    'author': 'Andrew Ross',
    'author_email': 'andrew.ross.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andrewrosss/snip-tsv',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
