# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['HtmlStyles']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'html-styles',
    'version': '0.1.2',
    'description': 'List of HTML tag default styles.',
    'long_description': '# HtmlStyles\n\nPython port of npm package [html-styles](https://www.npmjs.com/package/html-styles).\n\nList of known HTML tag default styles.\n\n## What is this?\n\nThis is a list of default styles for HTML tags as defined by [W3C specification](https://www.w3.org/TR/html5/rendering.html).\n\n\n## Install\n\n```sh\npip install html-styles\n```\n\n## Use\n\n```py\nfrom HtmlStyles import html_styles\nfrom itertools import chain\n\n\ndef get_tag_style(style):\n\n    return dict(\n        chain(\n            *map(\n                dict.items,\n                [\n                    {y: x["style"].get(style) for y in x["selectorText"].split(",")}\n                    for x in list(\n                        filter(lambda x: x["style"].get(style) is not None, html_styles)\n                    )\n                ],\n            )\n        )\n    )\n\n\nprint(get_tag_style("display"))\n\nprint(get_tag_style("white-space"))\n```\n\nYields:\n\n```py\n{\'[hidden]\': \'none\', \' area\': \'none\', \' base\': \'none\', \' basefont\': \'none\', \' datalist\': \'none\', \' head\': \'none\', \' link\': \'none\', \' meta\': \'none\', \'\\nnoembed\': \'none\', \' noframes\': \'none\', \' param\': \'none\', \' rp\': \'none\', \' script\': \'none\', \' source\': \'none\', \' style\': \'none\', \' template\': \'none\', \' track\': \'none\', \' title\': \'none\', \'embed[hidden]\': \'inline\', \'input[type=hidden i]\': \'none\', \'html\': \'block\', \' body\': \'block\', \'address\': \'block\', \' blockquote\': \'block\', \' center\': \'block\', \' div\': \'block\', \' figure\': \'block\', \' figcaption\': \'block\', \' footer\': \'block\', \' form\': \'block\', \' header\': \'block\', \' hr\': \'block\', \'\\nlegend\': \'block\', \' listing\': \'block\', \' main\': \'block\', \' p\': \'block\', \' plaintext\': \'block\', \' pre\': \'block\', \' xmp\': \'block\', \'dialog:not([open])\': \'none\', \'slot\': \'contents\', \'ruby\': \'ruby\', \'rt\': \'ruby-text\', \'article\': \'block\', \' aside\': \'block\', \' h1\': \'block\', \' h2\': \'block\', \' h3\': \'block\', \' h4\': \'block\', \' h5\': \'block\', \' h6\': \'block\', \' hgroup\': \'block\', \' nav\': \'block\', \' section\': \'block\', \'dir\': \'block\', \' dd\': \'block\', \' dl\': \'block\', \' dt\': \'block\', \' ol\': \'block\', \' ul\': \'block\', \'li\': \'list-item\', \'table\': \'table\', \'caption\': \'table-caption\', \'colgroup\': \'table-column-group\', \' colgroup[hidden]\': \'table-column-group\', \'col\': \'table-column\', \' col[hidden]\': \'table-column\', \'thead\': \'table-header-group\', \' thead[hidden]\': \'table-header-group\', \'tbody\': \'table-row-group\', \' tbody[hidden]\': \'table-row-group\', \'tfoot\': \'table-footer-group\', \' tfoot[hidden]\': \'table-footer-group\', \'tr\': \'table-row\', \' tr[hidden]\': \'table-row\', \'td\': \'table-cell\', \' th\': \'table-cell\', \' td[hidden]\': \'table-cell\', \' th[hidden]\': \'table-cell\', \'table > form\': \'none\', \' thead > form\': \'none\', \' tbody > form\': \'none\', \' tfoot > form\': \'none\', \' tr > form\': \'none\', \'fieldset\': \'block\'}\n{\'listing\': \'pre\', \' plaintext\': \'pre\', \' pre\': \'pre\', \' xmp\': \'pre\', \'pre[wrap]\': \'pre-wrap\', \'nobr\': \'nowrap\', \'nobr wbr\': \'normal\', \'td[nowrap]\': \'nowrap\', \' th[nowrap]\': \'nowrap\', \'table\': \'initial\', \'textarea\': \'pre-wrap\'}\n```\n## License\n\n[GPL][license] © Riverside Healthcare\nPorted from `html-styles` [MIT][license] © [Mario Nebl](https://github.com/marionebl)\n\n[license]: LICENSE',
    'author': 'Christopher Pickering',
    'author_email': 'cpickering@rhc.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Riverside-Healthcare/html-styles',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
