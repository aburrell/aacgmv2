
Changelog
=========
2.4.2 (2018-05-21)
-----------------------------------------
* Fixed bug in convert_mlt that caused all time inputs to occur
  at 00:00:00 UT
* Fixed year of last two updates in changelog


2.4.1 (2018-04-04)
-----------------------------------------
* Fix bug in installation that caused files to be placed in the wrong
  directory
* Added DOI

2.4.0 (2018-03-21)
-----------------------------------------

* Update to use AACGM-v2.4, which includes changes to the inverse MLT and
  dipole tilt functions and some minor bug fixes
* Updated file structure
* Updated methods, retaining old methods in deprecated module
* Added testing for python 3.6
* Updated dependencies, removing support for python 3.3
* Tested on Mac OSX
* Updated comments to include units for input and output
  
2.0.0 (2016-11-03)
-----------------------------------------

* Change method of calculating MLT, see documentation of convert_mlt for details


1.0.13 (2015-10-30)
-----------------------------------------

* Correctly convert output of subsol() to geodetic coordinates (the error in MLT/mlon conversion was not large, typically two decimal places and below)


1.0.12 (2015-10-26)
-----------------------------------------

* Return nan in forbidden region instead of throwing exception


1.0.11 (2015-10-26)
-----------------------------------------

* Fix bug in subsolar/MLT conversion


1.0.10 (2015-10-08)
-----------------------------------------

* No code changes, debugged automatic build/upload process and needed new version numbers along the way


1.0.0 (2015-10-07)
-----------------------------------------

* Initial release
