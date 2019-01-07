=============
Release Notes
=============

2.4
-----
* Bump Django dependency requirement to avoid vulnerable Django versions

2.3
-----

* Support Django 2.1+
* Remove duplicate hash calculation
* Always lower filename extensions


2.2
-----
* get_available_filename() now returns the default filename instead of raising
an exception, for compatibility with other packages (overridden by the hashed
filename on save)

2.1
-----
* Fix bug for bytes content
* Update setup.py and tox to support Django 2.0 for python version >= 3.4

2.0.1
-----
* Specify django <2.0 in setup.py


2.0
-----

* Add support for Python 3.5 and 3.6
* Drop support for Python 2.6
* Drop support for Django <1.8
* Use pytest and tox for testing
* Set up CI with travis
