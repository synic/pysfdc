#!/usr/bin/env python

from setuptools import find_packages, setup

import pysfdc

setup(
    name='pysfdc',
    version=pysfdc.__version__,
    description='SalesForce Integration Library',
    author=pysfdc.__author__,
    packages=find_packages(exclude=['test/*']),
    python_requires='>=3.8.0',
    install_requires=[
        # C Foreign Function Interface for Python, installed here explicitly
        # even though it's an automatically installed dependency of
        # simple-salesforce. The reason is that the automatically installed
        # version has a `ModuleMotFoundError`
        # License: MIT
        # https://github.com/cffi/cffi/blob/v0.23.0/COPYRIGHT
        "cffi==1.14.3",
        # String transformation library
        # License: MIT
        # https://github.com/jpvanhal/inflection/blob/0.5.0/LICENSE/
        'inflection==0.5.0',
        # low level salesforce interface
        # License: Apache 2.0
        # https://github.com/simple-salesforce/simple-salesforce/blob/v1.10.1/LICENSE.txt
        'simple-salesforce==1.10.1',
    ],
    extras_require={
        'debug': [
            # A better interactive shell
            # License: BSD 3-clause
            # https://github.com/ipython/ipython/blob/7.15.0/LICENSE
            'ipython==7.15.0',
        ],
        'testing': [
            # Style checker
            # License: MIT
            # https://github.com/PyCQA/flake8/blob/3.8.2/LICENSE
            'flake8==3.8.2',
            # Lint blind catch-all `except` statements
            # License: MIT
            # https://github.com/elijahandrews/flake8-blind-except/blob/v0.1.1/LICENSE
            'flake8-blind-except==0.1.1',
            # Lint built-ins names being used as variables
            # License: GPL v2
            # https://github.com/gforcada/flake8-builtins/blob/1.5.3/LICENSE
            'flake8-builtins==1.5.3',
            # Lint docstrings
            # License: MIT
            # https://github.com/PyCQA/flake8-docstrings/blob/1.5.0/LICENSE
            'flake8-docstrings==1.5.0',
            # Lint import order (alphabetical & logical)
            # License: GPL v3
            # https://github.com/PyCQA/flake8-import-order/blob/0.18.1/COPYING
            'flake8-import-order==0.18.1',
            # Test Suite
            # License: MIT
            # https://github.com/pytest-dev/pytest/blob/5.4.3/LICENSE
            'pytest==5.4.3',
        ],
    },
)
