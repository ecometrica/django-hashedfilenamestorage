#!/usr/bin/env python
import sys

from setuptools import setup


if sys.version_info < (3, 4):
    install_requires = ['Django>=1.8,<2.0']
else:
    install_requires = ['Django>=1.8,!=2.0,!=2.0.1,!=2.0.2,!=2.0.3,!=2.0.4,!=2.0.5,!=2.0.6,!=2.0.7,!=2.0.8,!=2.0.9']


setup(
    name='django-hashedfilenamestorage',
    version='2.4.1',
    description=('A Django storage backend that names files by hash value.'),
    long_description=open('README.rst', 'r').read(),
    author='Ecometrica',
    author_email='info@ecometrica.com',
    url='http://github.com/ecometrica/django-hashedfilenamestorage/',
    packages=['django_hashedfilenamestorage'],
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
    ],
    zip_safe=True,
    tests_require=['pytest', 'tox']
)
