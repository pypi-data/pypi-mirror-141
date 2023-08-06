# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asherah']

package_data = \
{'': ['*'], 'asherah': ['libasherah/*']}

install_requires = \
['cobhan>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'asherah',
    'version': '0.1.0',
    'description': 'Asherah envelope encryption and key rotation library',
    'long_description': '# asherah-python\n\nAsherah envelope encryption and key rotation library\n\nThis is a wrapper of the Asherah Go implementation using the Cobhan FFI library\n\nExample code:\n\n```python\nfrom asherah import Asherah, AsherahConfig\n\nconfig = AsherahConfig(\n    kms_type=\'static\',\n    metastore=\'memory\',\n    service_name=\'TestService\',\n    product_id=\'TestProduct\',\n    verbose=True,\n    session_cache=True\n)\ncrypt = Asherah()\ncrypt.setup(config)\n\ndata = b"mysecretdata"\n\nencrypted = crypt.encrypt("partition", data)\nprint(encrypted)\n\ndecrypted = crypt.decrypt("partition", encrypted)\nprint(decrypted)\n```\n',
    'author': 'Jeremiah Gowdy',
    'author_email': 'jeremiah@gowdy.me',
    'maintainer': 'GoDaddy',
    'maintainer_email': 'oss@godaddy.com',
    'url': 'https://github.com/godaddy/asherah-python/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
