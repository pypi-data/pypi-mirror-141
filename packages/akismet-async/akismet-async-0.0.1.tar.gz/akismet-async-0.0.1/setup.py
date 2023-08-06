# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['akismet']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0', 'strenum==0.4.7']

setup_kwargs = {
    'name': 'akismet-async',
    'version': '0.0.1',
    'description': 'An async Python interface to the Akismet API.',
    'long_description': 'akismet-async\n=========\n\nAn asyncronous Python 3 Akismet client library.\n\n## Installation\n```\npip install akismet-async\n```\n\n## API key verification\nGet your Akismet API key [here](http://akismet.com/plans/).\n```python\nfrom akismet import Akismet, Comment\n\nakismet_client = Akismet(api_key="YOUR_AKISMET_API_KEY" blog="http://your.blog/",\n                user_agent="My App/1.0.0")\n\nawait akismet_client.verify_key()\n```\n\n## Example usage\nYou can check a comment\'s spam score by creating a dictionary or a `Comment()` object\nfor greater type safety:\n```python\nfrom akismet import Akismet, Comment\n\nakismet_client = Akismet(api_key="YOUR_AKISMET_API_KEY" blog="http://your.blog/",\n                user_agent="My App/1.0.0")\n\ncomment = Comment(\n    comment_content="This is the body of the comment",\n    user_ip="127.0.0.1",\n    user_agent="some-user-agent",\n    referrer="unknown"\n)\n\nfirst_spam_status = await akismet_client.check(comment)\n\nsecond_spam_status = await akismet_client.check(\n    {\n        "user_ip": "127.0.0.2",\n        "user_agent": "another-user-agent",\n        "referrer": "unknown",\n        "comment_content": "This is the body of another comment",\n        "comment_author": \'John Doe\',\n        "is_test": True,\n    }\n)\n```\n`check()` returns one of the following strings:\n* `ham`\n* `probable_spam`\n* `definite_spam`\n* `unknown`\n\n### Submit Ham\nIf you have determined that a reported comment is not spam, you can report\nthe false positive to Akismet:\n```python\nawait akismet_client.submit_ham(comment)\n```\n\n### Submit Spam\nIf a spam comment passes the Akismet check, report it to Akismet:\n```python\nawait akismet_client.submit_spam(comment)\n```\n',
    'author': 'Arni Inaba Kjartansson',
    'author_email': 'arni@inaba.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arni-inaba/akismet-async',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
