
AACGM v2 Software C

Instructions:

1. Download the coefficients and put them in a convenient directory

2. Set the environment variable AACGM_v2_DAT_PREFIX to the directory that
   you are storing the coefficients in AND include the prefix of the
   coefficient files, i.e., aacgm_coeffs-12-

   e.g.:

   AACGM_v2_DAT_PREFIX=/mnt/thayerfs/shepherd/AACGM/idl/coeffs/aacgm_coeffs-12-

   Note that if you used the old AACGM software from JHU/APL you should have
   a similar variable already set.

3. Untar the contents of the .tar file into a directory

4. Build the test program by running:

   gcc -o test_aacgm test_aacgm.c aacgmlib_v2.c igrflib.c genmag.c -lm -static

   Note that on older systems you might need to remove the -static flag

5. Run the test program by running:

   test_aacgm

   The output should look something like:


***************************************************************************
* AACGM v2 ERROR: No Date/Time Set                                        *
*                                                                         *
* You must specifiy the date and time in order to use AACGM coordinates,  *
* which depend on the internal (IGRF) magnetic field. Before calling      *
* AACGM_v2_Convert() you must set the date and time to the integer values *
* using the function:                                                     *
*                                                                         *
*   AACGM_v2_SetDateTime(year,month,day,hour,minute,second);              *
*                                                                         *
* or to the current computer time in UT using the function:               *
*                                                                         *
*   AACGM_v2_SetNow();                                                    *
*                                                                         *
* subsequent calls to AACGM_v2_Convert() will use the last date and time  *
* that was set, so update to the actual date and time that is desired.    *
***************************************************************************


Setting time to : 20140322 0311:00
lat = 45.500000, lon = -23.500000, height = 1135.000000
mlat = 48.377539, mlon = 57.822458, r = 1.000000


lat = 45.500000, lon = -23.500000, height = 1135.000000
mlat = 49.425800, mlon = 58.259686, r = 1.000000


lat = 65.500000, lon = 93.500000, height = 1135.000000
mlat = 62.251076, mlon = 166.990581, r = 1.000000


lat = 65.500000, lon = 93.500000, height = 0.000000
mlat = 60.799240, mlon = 166.518084, r = 1.000000


lat = 75.500000, lon = 73.500000, height = 0.000000
mlat = 70.420669, mlon = 150.743259, r = 1.000000


lat = 75.500000, lon = 73.500000, height = 0.000000
mlat = 70.726381, mlon = 150.672892, r = 1.000000


IMPORTANT NOTES:

1. The function AACGM_v2_Convert is a direct replacement for the function
   AACGMConvert that is used in much of the SD software. This is your
   starting point, but you can modify the test program as you like.

2. New user-space functions have been added that allow users to set the
   date and time. The functions are:

       AACGM_v2_SetDateTime(int year, int month, int day, int hour,
                        int minute, int second);

       AACGM_v2_SetNow();

   The latter will use the current computer date and time in UT.

   Note that setting the time frequently triggers an interpolation in time and
   in altitude, which will slow the calculations. Testing should be done to
   determine what the correspondence between changes in time and AACGM lat/lon
   are.

3. You must set the date and time at least once or the code will not run.

4. A new user-space function has been added that allow users to see what
   date and time are being used. The function is:

       AACGM_v2_GetDateTime(int *year, int *month, int *day, int *hour,
                        int *minute, int *second, int *doy);

