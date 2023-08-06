# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['svgreplicate']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['svgreplicate = svgreplicate.__main__:main']}

setup_kwargs = {
    'name': 'svgreplicate',
    'version': '0.1.1',
    'description': 'Tool for batch modifying and replicating SVG-files',
    'long_description': '# SVGReplicate \n\nTool for batch modifying and replicating SVG files. \n\n## Installation \n\nInstall from PyPI by running `pip install svgreplicate`.\n\n## Usage\n\nCreate an SVG file, either by hand or with your favorite vector graphics tool, like [InkScape](https://inkscape.org):\n\n```xml\n<svg\n    width="210mm"\n    height="297mm" \n    id="svg" \n    version="1.1"\n    xmlns="http://www.w3.org/2000/svg" >\n    <g id="group1">\n        <ellipse\n            style="opacity:1;fill:#009bff"\n            id="ellipse1"\n            cx="0.0"\n            cy="0.0"\n            rx="10.0"\n            ry="10.0" />\n        <g id="group2" />\n    <text id="text1">\n        <tspan>First text</tspan>\n        <tspan>Second text \n            <tspan>Nested text</tspan> \n        </tspan>\n    </text>\n    </g>\n</svg>\n```\n\nNext, create a json with the replicas you want: \n\n```json\n[\n    {\n        "filename": "example/replica1.svg", \n        "modifications": [\n        \t{"id": "ellipse1", "style": {"fill": "#000000", "display": "none"}},\n        \t{"id": "group2", "style": {"display": "none"}},\n        \t{"id": "text1", "text": "Hello, world!"}\n        ]\n    },\n    {\n        "filename": "example/replica2.svg",\n        "modifications": [\n                {"id": "ellipse1", "style": {"fill": "#ffffff", "display": "none"}},\n                {"id": "group2", "style": {"display": "none"}},\n                {"id": "text1", "text": "Here\'s Johnny!"}\n        ]\n    }\n]\n```\n\nAnd finally, run the script:\n\n```bash \nsvgreplicate --filename path-to-svg-template.svg --replicas path-to-replicas-config.json \n```\n\nYou now have 2 files in the example folder, based on the template, with the specified modifications. \n\n## Backlog \n\nIn future, I\'d like to add at least the functionality for automatically rendering to PNG. \n\n',
    'author': 'Jan Hein de Jong',
    'author_email': 'janhein.dejong@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/janheindejong/svgreplicate',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
