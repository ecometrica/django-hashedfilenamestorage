#!/usr/bin/env python
from distutils.core import setup

setup(
    name='livingbio-django-hashedfilenamestorage',
    version='2.0',
    description=('A Django storage backend that names files by hash value.'),
    long_description=open('README.rst', 'r').read(),
    author='Ecometrica',
    author_email='info@ecometrica.com',
    url='http://github.com/ecometrica/django-hashedfilenamestorage/',
    packages=['django_hashedfilenamestorage'],
    install_requires=['Django>=1.3'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
    ],
    zip_safe=True,
)
