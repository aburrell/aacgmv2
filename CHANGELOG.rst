
Changelog
=========

2.6.2 (2020-01-13)
------------------

* Drop support for EOL Python 2.7 and added testing for Python 3.9
* Added a .zenodo.json file
* Fixed AppVeyor environment

2.6.1 (2020-09-11)
------------------

* Moved formerly deprecated utilities from `deprecated.py` to `utils.py`
* Removed allowance for deprecated kwarg `code` from `convert_latlon` and
  `convert_latlon_arr`, as scheduled
* Updated CI to include Python 3.8 everywhere
* Moved all configuration information to setup.cfg
* Fixed coveralls implementation
* Fixed broken links in the documentation
* Removed unused code analysis tools
* Improved unit test coverage
* Make PEP8 changes


2.6.0 (2020-01-06)
------------------

* Updated AACGM-v2 coefficients derived using the IGRF13 model
* Updated IGRF and GUFM1 coefficients using the IGRF13 model
* Added additional checks to the C code for reading the IGRF13 coefficient file
* Removed `convert` routine in `deprecated.py`
* Pushed back keyword argument deprecation of `code`
* Scheduled deprecation for remaining routines in `deprecated.py`
* Parametrized several unit tests
* Updated `README.md` examples
* Updated CI to include python 3.8
  

2.5.3 (2019-12-23)
------------------

* Changed log warning about array functions to info
* Changed default method from `TRACE` to `ALLOWTRACE`
* Added C wrappers for list input, removing inefficient use of `np.vectorize`
* Fixed documentation for use of `method_code`
* Added FutureWarning for deprecated use of `code` keyword argument
* Updated previous version's changelog to encompass all changes
* Improved docstrings to make documentation easier to read
* Removed failing twine commands from `appveyor.yml`
* Removed `RuntimeWarning` filter from `tox.ini`


2.5.2 (2019-08-27)
------------------

* Added FutureWarning to deprecated functions
* Updated names in licenses
* Moved module structure routine tests to their own class
* Added high altitude limit to avoid while-loop hanging
* Changed version support to 2.7, 3.6, and 3.7
* Removed logbook dependency
* Added logic to avoid reseting environment variables if not necessary
* Added copyright and license disclaimer to module-specific program files
* Changed keyword argument `code` to `method_code`
  

2.5.1 (2018-10-19)
------------------

* Commented out debug statement in C code
* Updated environment variable warning to output to stderr instead of stdout
* Added templates for pull requests, issues, and a code of conduct


2.5.0 (2018-08-08)
------------------

* Updated C code and coefficients to version 2.5.  Changes in python
  code reflect changes in C code (includes going back to using environment
  variables instead of strings for coefficient file locations)
* Added decorators to some of the test functions
* Specified AppVeyor Visual Studio version, since it was defaulting to 2010 and
  that version doesn't work with python 3


2.4.2 (2018-05-21)
------------------

* Fixed bug in convert_mlt that caused all time inputs to occur
  at 00:00:00 UT
* Fixed year of last two updates in changelog


2.4.1 (2018-04-04)
------------------

* Fix bug in installation that caused files to be placed in the wrong
  directory
* Added DOI


2.4.0 (2018-03-21)
------------------

* Update to use AACGM-v2.4, which includes changes to the inverse MLT and
  dipole tilt functions and some minor bug fixes
* Updated file structure
* Updated methods, retaining old methods in deprecated module
* Added testing for python 3.6
* Updated dependencies, removing support for python 3.3
* Tested on Mac OSX
* Updated comments to include units for input and output


2.0.0 (2016-11-03)
------------------

* Change method of calculating MLT, see documentation of convert_mlt for details


1.0.13 (2015-10-30)
-------------------

* Correctly convert output of subsol() to geodetic coordinates (the error in
  MLT/mlon conversion was not large, typically two decimal places and below)


1.0.12 (2015-10-26)
-------------------

* Return nan in forbidden region instead of throwing exception


1.0.11 (2015-10-26)
-------------------

* Fix bug in subsolar/MLT conversion


1.0.10 (2015-10-08)
-------------------

* No code changes, debugged automatic build/upload process and needed new
  version numbers along the way


1.0.0 (2015-10-07)
------------------

* Initial release
