# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ietf_reviewtool']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'charset-normalizer>=2.0.6,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'language-tool-python>=2.5.3,<3.0.0',
 'num2words>=0.5.10,<0.6.0',
 'requests-cache>=0.5.2,<0.6.0',
 'urlextract>=1.5.0,<2.0.0']

entry_points = \
{'console_scripts': ['ietf-reviewtool = ietf_reviewtool.ietf_reviewtool:cli',
                     'irt = ietf_reviewtool.ietf_reviewtool:cli']}

setup_kwargs = {
    'name': 'ietf-reviewtool',
    'version': '0.2.0',
    'description': 'Review tool for IETF documents',
    'long_description': '# ietf-reviewtool\n\nThis is a simple Python 3 tool to download and review IETF documents, such as\nInternet-Drafts or RFCs, and comes packaged as a single `ietf-reviewtool`\nscript.\n\n## About\n\n`ietf-reviewtool` offers several different review tools:\n\n* `fetch` downloads items (I-Ds, charters, RFCs, etc.) for review\n\n* `fetch-agenda` downloads all items on the [agenda of the next IESG\n  telechat](https://datatracker.ietf.org/iesg/agenda/) for review\n\n* `strip` strips headers, footers and pagination from items, similar to the\n  earlier [`rfcstrip`](https://tools.ietf.org/tools/rfcstrip/about) tool\n\n* `review` extracts inline reviews from the indicated items and formats them for\n  sharing by email or submission to the [IETF\n  datatracker](https://datatracker.ietf.org/), with some functionality that is\n  similar to the earlier\n  [`idcomments`](https://tools.ietf.org/tools/idcomments/about) tool\n\nThis is a work in progress. Additional functionality will be added over time, so\nthere is a chance this documentation only covers a subset of what the actual\ntool offers. You can get command line help on the various tools by passing\n`--help` to `ietf-reviewtool` and its sub-tools.\n\n## Installation\n\nYou can install this via [PyPI](https://pypi.org/project/ietf-reviewtool/):\n\n``` shell\npip install ietf-reviewtool\n```\n\n## Usage\n\nAn example workflow of the tool is as follows.\n\n### Downloading items\n\nYou first download the item for review:\n``` shell\nietf-reviewtool fetch rfc1925.txt\n```\n\nThis downloads the text version of\n[RFC1925](https://datatracker.ietf.org/doc/html/rfc1925) into a text file named\n`rfc1925.txt` and (by default) performs a `strip` operation on the file.\n\nYou will then open the stripped `rfc1925.txt` for review in your preferred text\neditor.\n\n### Reviewing\n\nYou can flag issues of three different severity levels, namely, "discuss",\n"comment" and "nit". (These levels are inspired by the [IESG review\nprocess](https://www.ietf.org/about/groups/iesg/statements/iesg-discuss-criteria/).)\n\nIn order to flag an issue of a given severity level, enter a new line at an\nappropriate location in the document that reads `DISCUSS:`, `COMMENT:` or\n`NIT:`.\n\n#### Inline issues\n\nUsing `rfc1925.txt` as an example and using `***` to indicate the added review\ncontent, you can flag an "inline" issue like this:\n```\n2. The Fundamental Truths\n\n   (1)  It Has To Work.\n\n***COMMENT: Well, duh.***\n```\n\nAfter saving the changed `rfc1925.txt`, you can then extract a formatted review\nas:\n\n```\nSection 2, paragraph 2, comment:\nWell, duh.\n```\n\nSee below for how to extract a review.\n\nUsing `DISCUSS:` or `NIT:` instead of `COMMENT:` will change the severity of the\nissue, as appropriate.\n\n#### Issues with context\n\nIt is possible quote part of the original document, to give the review some context, like this:\n\n```\n***COMMENT:***\n   (3)  With sufficient thrust, pigs fly just fine. However, this is\n***Can we stop picking on pigs or pigeons?***\n```\n\nThis will produce the following review:\n\n```\nSection 2, paragraph 5, comment:\n>    (3)  With sufficient thrust, pigs fly just fine. However, this is\n\nCan we stop picking on pigs or pigeons?\n```\n\n#### Inline nits\n\nTo quickly flag some editing nits, such as spelling errors, you can simply edit\nthe text directly, correcting the nit. For example, to flag an existing spelling error in `rfc1925.txt` (where "agglutinate" is misspelled as "aglutenate"), you would simply correct the word in the text:\n\n```\n   (5)  It is always possible to ***agglutinate*** multiple separate problems\n        into a single complex interdependent solution. In most cases\n        this is a bad idea.\n```\n\nWhen extracting the formatted review, such inline corrections are added to the "nits" section in "diff" format:\n\n```\nSection 2, paragraph 7, nit:\n-    (5)  It is always possible to aglutenate multiple separate problems\n-                                       ^\n+    (5)  It is always possible to agglutinate multiple separate problems\n+                                    +   ^\n```\n\n### Extracting the review\n\nAfter editing a source file, you can extract a formatted review with:\n``` shell\nietf-reviewtool review rfc1925.txt\n```\n\nWith the given example, this would result in the following output:\n```\n-------------------------------------------------------------------------\nCOMMENT\n-------------------------------------------------------------------------\nSection 2, paragraph 2, comment:\nWell, duh.\n\nSection 2, paragraph 5, comment:\n>    (3)  With sufficient thrust, pigs fly just fine. However, this is\n\nCan we not always pick on pigs or pigeons?\n\n-------------------------------------------------------------------------\nNIT\n-------------------------------------------------------------------------\nSection 2, paragraph 7, nit:\n-    (5)  It is always possible to aglutenate multiple separate problems\n-                                       ^\n+    (5)  It is always possible to agglutinate multiple separate problems\n+                                    +   ^\n```\n\n### Using caches\n\nIn order to speed up the process, and to operate while being offline, you can\nset various environment variables to point the tool at directories in which you\n[cache various IETF document via\n`rsync`](https://www.ietf.org/standards/ids/internet-draft-mirror-sites/).\n\nThese environment variables are named:\n\n* `IETF_CHARTERS`\n* `IETF_CONFLICT_REVIEWS`\n* `IETF_IDS`\n* `IETF_RFCS`\n* `IETF_STATUS_CHANGES`\n\nWhen the tool finds a given item to review in the cache, it will refrain from\ndownloading it from the web.\n\nNote that the tool will **not** place items into the cache directories when they are not present; you **will** need to update the cache via `rsync`.\n\n## Acknowledgments\n\nThe ideas for some of these tools came from some of Henrik Levkowetz\'s earlier\n`bash` scripts. In the case of the `strip` tool, most of the original regular\nexpressions were taken from his\n[`rfcstrip`](https://tools.ietf.org/tools/rfcstrip/about) `awk` script.\n\n\n## License\n\nCopyright (C) 2021-2022  Lars Eggert\n\nThis program is free software; you can redistribute it and/or modify it under\nthe terms of the GNU General Public License as published by the Free Software\nFoundation; either version 2 of the License, or (at your option) any later\nversion.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY\nWARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A\nPARTICULAR PURPOSE.  See the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along with\nthis program; if not, write to the Free Software Foundation, Inc., 51 Franklin\nStreet, Fifth Floor, Boston, MA  02110-1301, USA.\n',
    'author': 'Lars Eggert',
    'author_email': 'lars@eggert.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/larseggert/ietf-reviewtool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
