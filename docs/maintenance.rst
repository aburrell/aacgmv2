Package Maintenance
===================

Updating IGRF
-------------

The `International Geomagnetic Reference Field <https://www.ngdc.noaa.gov/IAGA/vmod/igrf.html>`_
is regularly updated to reflect the most recent changes to the Terrestrial
magnetic field. AACGMV2 currently uses IRGF-14 coefficients, which are provided
in the ``aacgmv2/aacgmv2/igrf14coeff.txt`` file and a combined magnetic model
that uses coefficients provided in ``aacgmv2/aacgmv2/magmodel_1590-2025.txt``.
To change or update the magnetic field coefficients used by AACGMV2, you need to
obtain the new IGRF coefficients, magnetic model coefficients, and the AACGMV2
coefficients, and update the Python and C code. If substantial changes have been
made to the C code, it may be necessary to update the functions in
``aacgmv2/aacgmv2/aacgmv2module.c``, as this is what allows Python to interface
with the AACGMV2 source code. Updates to the AACGMV2 coefficients and code may
be obtained from the website hosted by
`Dartmouth <https://superdarn.thayer.dartmouth.edu/aacgm.html>`_.  The C tarball
contains the IGRF and magnetic model coefficient files.

Assuming no changes were made to the way coefficients are handled or the C code
is called, the updating process is simple:

1. Clone the repository or update your fork of the repository
   (see :ref:`contributing`).
2. Replace the AACGMV2 coefficients in ``aacgmv2/aacgmv2/aacgm_coeffs``.
3. Replace the IGRF coefficient file in ``aacgmv2/aacgmv2/``.
4. Update the ``aacgmv2/__init__.py`` global variables ``AACGM_v2_DAT_PREFIX``
   and ``IGRF_COEFFFS``
5. If the C code has been updated, update the ``c_aacgmv2/README.txt``,
   ``c_aacgmv2/release_notes.txt``, and ``LISCENCE-AstAlg.txt`` files for the
   new version.
6. If the C code has been updated, update the header files in
   ``c_aacgmv2/include``. Check to see if any files have been removed. If
   ``c_aacgmv2/include/astalg.h`` ends up removing the ``M_PI`` definition, add
   it back in (needed for Windows).
7. If the C code has been updated, update the source files in ``c_aacgmv2/src``.
   Check to see if any files have been removed; remove them from the list of
   ``aacgmv2/setup.py`` sources. If the ``NAN`` and ``isfinite``
   definitions are removed from ``mlt_v2.c`` and the ``EINVAL`` definition and
   ``setenv`` function are removed from ``rtime.c``, add these and the header
   info back in (needed for Windows). Also, fix the commenting style in
   ``test_aacgm.c`` to reduce compiler warnings.
8. Rebuild and install AACGMV2 following the instructions in
   :ref:`installation`.
9. Update the unit tests in the ``aacgmv2/aacgmv2/tests/`` directory so that
   they check the functions are working correctly with dates after the IGRF
   epoch update. You will have to update the hard-coded confirmation values
   used by these tests, but the values should not change by more than a
   hundredth of a degree.  Tests that may need to be updated include:

   
   A. ``test_c_aacgmv2.py::TestCAACGMV2.test_convert``
   B. ``test_cmd_aacgmv2.py::TestCmdAACGMV2::test_convert_stdin_stdout``
   C. ``test_cmd_aacgmv2.py::TestCmdAACGMV2::test_convert_mlt_stdin_stdout``
   D. ``test_struct_aacgmv2.py::TestTopVariables::test_top_parameters``
   E. ``test_utils_aacgmv2.py::TestUtilsAACGMV2::test_igrf_dipole_axis``
   F. ``environ/test_environ_aacgmv2.py::TestPyEnviron``

      
10. Commit all changes and create a pull request on GitHub to integrate your 
    branch with updated IGRF into the main repository.

Modifying the C Source
----------------------
When modifying the C source code, it can be helpful to run a preliminary
validation of the C output independent of the Python wrapper. This should
be done within the ``aacgmv2/c_aacgmv2`` directory.

1. Build the ``test_aacgm`` binary by following the instructions in
   ``aacgmv2/c_aacgmv2/README.txt``.  You will have to alter the compilation
   command to preface each ``.c`` file with ``src`` and also add ``-Iinclude``.
3. Execute the ``test_aacgm`` binary.
4. Confirm the output printed to the screen matches the test output shown in
   the comment block provided in the ``aacgmv2/c_aacgmv2/README.txt``.
5. If the modifications involved adding or removing C source files, modify
   the list of extension sources in ``setup.py``.
6. Rebuild and install AACGMV2 following the instructions in
   :ref:`installation`.
