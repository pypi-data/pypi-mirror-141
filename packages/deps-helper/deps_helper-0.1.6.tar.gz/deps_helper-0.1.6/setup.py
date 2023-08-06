# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['deps_helper']
setup_kwargs = {
    'name': 'deps-helper',
    'version': '0.1.6',
    'description': 'dependencies helper',
    'long_description': '# dependency helper\n\n[![Supported Python Versions](https://img.shields.io/pypi/pyversions/deps-helper/0.1.6)](https://pypi.org/project/deps-helper/) [![PyPI version](https://badge.fury.io/py/deps-helper.svg)](https://badge.fury.io/py/deps-helper)\n\nDependency helper for properties of python class\n\n```$ pip install deps_helper```\n\n```python\nfrom deps_helper import Dependencies\n\n\nclass A(deps := Dependencies.new()):\n    @deps.register(_for="operation")\n    def requested_by(self, user):\n        print(f"operation requested by {user}.")\n\n        return f"requested by {user}"\n\n    @deps.register(_for=["check_validity", "operation"])\n    def validity(*_):\n        ...\n\n    @deps.guard()\n    def operation(self):\n        print("execute operation...")\n\n    @deps.guard()\n    def check_validity(self):\n        if self.validity:\n            print("Ok")\n\n\n>>> a = A()\n>>> a.check_validity()\nTraceback (most recent call last):\n...\nAttributeError: ("follow attributes are not assigned for check_validity => ", [validity])\n>>> a.operation()\nTraceback (most recent call last):\n...\nAttributeError: ("follow attributes are not assigned for operation => ", [requested_by, validity])\n>>> a.validity = True\n>>> a.check_validity()\nOk\n>>> a.requested_by = "admin"\noperation requested by admin.\n>>> a.operation()\nexecute operation...\n>>> print(a.requested_by)\nrequested by admin\n>>>\n```\n',
    'author': 'jasonyun',
    'author_email': 'killa30865@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ja-sonYun/deps_helper',
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
