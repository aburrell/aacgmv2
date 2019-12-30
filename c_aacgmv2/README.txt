AACGM-v2 Software
v2.6 20191228

C Instructions:

1. Download the coefficients and put them in a convenient directory

2. Set the environment variable AACGM_v2_DAT_PREFIX to the directory that
   you are storing the coefficients in AND include the prefix of the
   coefficient files, i.e., aacgm_coeffs-13-

   e.g.:

   AACGM_v2_DAT_PREFIX=/mnt/thayerfs/shepherd/AACGM/idl/coeffs/aacgm_coeffs-13-

   Note that if you used the old AACGM software from JHU/APL you should have
   a similar variable already set.

3. Untar the contents of the .tar file into a directory

4. Setup the magnetic field model by putting the GUFM1/IGRF coefficients file
   (magmodel_1590-2020.txt) somewhere or leaving them in the current directory
   and setting the environment variable IGRF_COEFFS to the fully qualified
   path, i.e.,

   IGRF_COEFFS=/directory_you_put_IGRF_coefs_in/magmodel_1590-2020.txt

5. Build the test program by running:

   gcc -o test_aacgm test_aacgm.c aacgmlib_v2.c igrflib.c genmag.c astalglib.c \
                         mlt_v2.c rtime.c -lm

6. Run the test program by running:

   test_aacgm

   The output should look something like:

================================================================================

AACGM-v2 Test Program

================================================================================

TEST: no date/time (this will return an error.)

**************************************************************************
* AACGM-v2 ERROR: No Date/Time Set                                       *
*                                                                        *
* You must specifiy the date and time in order to use AACGM coordinates, *
* which depend on the internal (IGRF) magnetic field. Before calling     *
* AACGM_v2_Convert() you must set the date and time to the integer values*
* using the function:                                                    *
*                                                                        *
*   AACGM_v2_SetDateTime(year,month,day,hour,minute,second);             *
*                                                                        *
* or to the current computer time in UT using the function:              *
*                                                                        *
*   AACGM_v2_SetNow();                                                   *
*                                                                        *
* subsequent calls to AACGM_v2_Convert() will use the last date and time *
* that was set, so update to the actual date and time that is desired.   *
**************************************************************************

TEST: Setting time to : 20240322 0311:00

TEST: geographic to AACGM-v2
     GLAT       GLON        HEIGHT       MLAT       MLON       R
     45.500000  -23.500000  1135.000000  47.588773  56.761655  1.177533

TEST: AACGM-v2 to geographic
     MLAT       MLON        HEIGHT       GLAT       GLON       HEIGHT
     47.588773  56.761655  1131.097495  45.439106  -23.475908  1134.977273

Do the same thing but use field-line tracing

TEST: geographic to AACGM-v2 (TRACE)
     GLAT       GLON        HEIGHT       MLAT       MLON       R
     45.500000  -23.500000  1135.000000  47.594236  56.760096  1.177533

TEST: AACGM-v2 to geographic (TRACE)
     MLAT       MLON        HEIGHT       GLAT       GLON       HEIGHT
     47.594236  56.760096  1131.097495  45.500002  -23.500000  1135.000001

--------------------------------------------------------------------------------

Testing MLT
--------------------------------------------------------------------------------

      GLAT       GLON        HEIGHT       MLAT       MLON       MLT
TRACE 37.000000  -88.000000  300.000000  48.839634  -17.004932  1.977822
COEFF 37.000000  -88.000000  300.000000  48.844360  -16.999467  1.978187


Array:
      45.0000   0.0000    150.0000     40.2851     76.6686      8.2227
      45.0000   1.0000    150.0000     40.2456     77.4908      8.2775
      45.0000   2.0000    150.0000     40.2116     78.3166      8.3326
      45.0000   3.0000    150.0000     40.1830     79.1461      8.3879
      45.0000   4.0000    150.0000     40.1594     79.9794      8.4434
      45.0000   5.0000    150.0000     40.1407     80.8166      8.4993
      45.0000   6.0000    150.0000     40.1267     81.6577      8.5553
      45.0000   7.0000    150.0000     40.1171     82.5029      8.6117
      45.0000   8.0000    150.0000     40.1116     83.3521      8.6683
      45.0000   9.0000    150.0000     40.1102     84.2055      8.7252
      45.0000  10.0000    150.0000     40.1125     85.0631      8.7824
      45.0000  11.0000    150.0000     40.1184     85.9250      8.8398
      45.0000  12.0000    150.0000     40.1275     86.7910      8.8976
      45.0000  13.0000    150.0000     40.1398     87.6614      8.9556
      45.0000  14.0000    150.0000     40.1550     88.5360      9.0139
      45.0000  15.0000    150.0000     40.1730     89.4149      9.0725
      45.0000  16.0000    150.0000     40.1934     90.2981      9.1314
      45.0000  17.0000    150.0000     40.2161     91.1856      9.1905
      45.0000  18.0000    150.0000     40.2409     92.0774      9.2500
      45.0000  19.0000    150.0000     40.2677     92.9734      9.3097


IMPORTANT NOTES:

1. Magnetic local time (MLT) functions have been restored:

      double MLTConvertYMDHMS_v2(int yr,int mo,int dy,int hr,int mt,int sc,
                      double mlon);
      double MLTConvertYrsec_v2(int yr,int yrsec, double mlon);
      double MLTConvertEpoch_v2(double epoch, double mlon);


   Note that AACGM-v2 longitude is much less sensitive to altitude; maximum
   difference of <1 degree (5 min in MLT) over the range 0-2000 km. For this
   reason there is no height passed directly into the MLT routines. The value
   of AACGM-v2 longitude does change with altitude and variations of MLT with
   altitude above a given geographic location do exist.

2. The function AACGM_v2_Convert is a direct replacement for the function
   AACGMConvert that is used in much of the SD software. This is your
   starting point, but you can modify the test program as you like.

3. New user-space functions have been added that allow users to set the
   date and time. The functions are:

       AACGM_v2_SetDateTime(int year, int month, int day, int hour,
                        int minute, int second);

       AACGM_v2_SetNow();

   The latter will use the current computer date and time in UT.

   Note that setting the time frequently triggers an interpolation in time and
   in altitude, which will slow the calculations. Testing should be done to
   determine what the correspondence between changes in time and AACGM lat/lon
   are.

4. You must set the date and time at least once or the code will not run.

5. A new user-space function has been added that allow users to see what
   date and time are being used. The function is:

       AACGM_v2_GetDateTime(int *year, int *month, int *day, int *hour,
                        int *minute, int *second, int *doy);


This package include the following files:

AACGM C software:

README.txt            ; this file
release_notes.txt     ; details of changes to v2.6
aacgmlib_v2.c         ; AACGM-v2 functions
aacgmlib_v2.h         ; AACGM-v2 header file
genmag.c              ; general purpose functions
genmag.h              ; general purpose header file
igrflib.c             ; internal IGRF functions
igrflib.h             ; internal IGRF header file
rtime.c               ; internal date/time functions
rtime.h               ; internal date/time header file
astalg.c              ; Astronomical algorithms functions
astalg.h              ; Astronomical algorithms header file
mlt_v2.c              ; MLT-v2 functions
mlt_v2.h              ; MLT-v2 header file
igrf13coeffs.txt      ; IGRF13 coefficients (1900-2020)
magmodel_1590-2020.txt; magnetic field coefficients (1590-2020)
test_aacgm.c          ; testing and example program
LICENSE-AstAlg.txt    ; license file for Astro algrorithms

