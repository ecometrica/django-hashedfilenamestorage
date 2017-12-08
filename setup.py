#!/usr/bin/env python
from distutils.core import setup

setup(
    name='django-hashedfilenamestorage',
    version='1.0',
    description=('A Django storage backend that names files by hash value.'),
    long_description=open('README.rst', 'r').read(),
    author='Ecometrica',
    author_email='info@ecometrica.com',
    url='http://github.com/ecometrica/django-hashedfilenamestorage/',
    packages=['django_hashedfilenamestorage'],
    install_requires=['Django>=1.8'],
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
        'Topic :: Software Development :: Libraries',
    ],
    zip_safe=True,
    tests_require=['pytest', 'tox']
)
