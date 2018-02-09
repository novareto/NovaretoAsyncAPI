# -*- coding: utf-8 -*-

import sys, os
from setuptools import setup, find_packages


version = '0.1'


setup(
    name='nv_async',
    version=version,
    description="",
    long_description=""" """,
    classifiers=[],
    keywords='',
    author='',
    author_email='',
    url='',
    license='',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "dolmen.api_engine",
        "sanic",
        "zeep",
        "zeep[async]",
        "zope.i18nmessageid",
    ],
)
