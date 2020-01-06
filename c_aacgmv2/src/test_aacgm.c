#include <stdio.h>
#include "aacgmlib_v2.h"
#include "mlt_v2.h"

#define CR printf("\n")
#define DEBUG 1

void next(void);
void line(char ch, int n);

int main(void)
{
double lat,lon,hgt;
double h, mlt_c, mlt_t;
double rtp[3];
double mlat,mlon,r;
int k, err, npts;
int yr, mo, dy, hr, mt, sc;

line('=',80);
printf("\nAACGM-v2 Test Program\n\n");
line('=',80);
CR;

/* compute AACGM-v2 lat/lon with no time specified */
printf("TEST: no date/time (this will return an error.)\n");
lat = 45.5;
lon = -23.5;
hgt = 1135.;
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A);
if (err == 0) {
  printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
  printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
  printf("\n\n");
}

#if (DEBUG > 1)
next();

printf("TEST: Setting time to : %04d%02d%02d %02d%02d:%02d  (will fail)\n", 1350,1,22,0,0,0);
AACGM_v2_SetDateTime(1350, 1, 22, 0,0,0); /* should fail */
printf("TEST: Setting time to : %04d%02d%02d %02d%02d:%02d\n", 1850,1,22,0,0,0);
AACGM_v2_SetDateTime(1850, 1, 22, 0,0,0); /* this is now valid */
printf("TEST: Setting time to : %04d%02d%02d %02d%02d:%02d\n", 1900,1,22,0,0,0);
AACGM_v2_SetDateTime(1900, 1, 22, 0,0,0); /* this is valid */
printf("TEST: Setting time to : %04d%02d%02d %02d%02d:%02d\n", 2020,1,22,0,0,0);
AACGM_v2_SetDateTime(2020, 1, 22, 0,0,0); /* this is now valid */
printf("TEST: Setting time to : %04d%02d%02d %02d%02d:%02d\n", 2019,1,22,0,0,0);
AACGM_v2_SetDateTime(2019, 1, 22, 0,0,0); /* this is valid */
printf("TEST: Setting time to : %04d%02d%02d %02d%02d:%02d  (will fail)\n", 2025,1,22,0,0,0);
AACGM_v2_SetDateTime(2025, 1, 22, 0,0,0); /* should fail*/
next();
#endif

yr = 2024;
mo = 3;
dy = 22;
hr = 3;
mt = 11;
sc = 0;
printf("TEST: Setting time to : %04d%02d%02d %02d%02d:%02d\n",
          yr, mo, dy, hr, mt, sc);
CR;

/* set date and time */
AACGM_v2_SetDateTime(yr, mo, dy, hr, mt, sc);

lat = 45.5;
lon = -23.5;
hgt = 1135.;

printf("TEST: geographic to AACGM-v2\n");
/* compute AACGM lat/lon */
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A);

printf("     GLAT       GLON        HEIGHT       MLAT       MLON       R\n");
printf("     %lf  %lf  %lf  %lf  %lf  %lf", lat,lon,hgt, mlat,mlon,r);
printf("\n\n");
#if (DEBUG > 1)
next();
#endif

printf("TEST: AACGM-v2 to geographic\n");
/* do the inverse: A2G */
hgt = (r-1.)*RE;
err = AACGM_v2_Convert(mlat,mlon,hgt, &lat,&lon, &h, A2G);

printf("     MLAT       MLON        HEIGHT       GLAT       GLON       HEIGHT\n");
printf("     %lf  %lf  %lf  %lf  %lf  %lf", mlat,mlon,hgt, lat,lon,h);
printf("\n\n");
#if (DEBUG > 1)
next();
#endif

/* same thing but using field-line tracing */
lat = 45.5;
lon = -23.5;
hgt = 1135.;

printf("Do the same thing but use field-line tracing\n\n");
printf("TEST: geographic to AACGM-v2 (TRACE)\n");
/* compute AACGM lat/lon */
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A|TRACE);

printf("     GLAT       GLON        HEIGHT       MLAT       MLON       R\n");
printf("     %lf  %lf  %lf  %lf  %lf  %lf", lat,lon,hgt, mlat,mlon,r);
printf("\n\n");
#if (DEBUG > 1)
next();
#endif

printf("TEST: AACGM-v2 to geographic (TRACE)\n");
/* do the inverse: A2G */
hgt = (r-1.)*RE;
err = AACGM_v2_Convert(mlat,mlon,hgt, &lat,&lon, &h, A2G|TRACE);

printf("     MLAT       MLON        HEIGHT       GLAT       GLON       HEIGHT\n");
printf("     %lf  %lf  %lf  %lf  %lf  %lf", mlat,mlon,hgt, lat,lon,h);
printf("\n\n");
#if (DEBUG > 1)
next();
#endif

/* compare tracing to coefficients */
lat = 45.5;
lon = -23.5;
hgt = 150.;

/* set date and time */
AACGM_v2_SetDateTime(2018,1,1,0,0,0);

#if (DEBUG >1)
printf("TEST: geographic to AACGM-v2; coefficients\n");
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A);
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
next();
#endif

#if (DEBUG > 1)
printf("TEST: geographic to AACGM-v2; tracing\n");
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A|TRACE);
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
next();
#endif

#if (DEBUG > 1)
printf("TEST: geographic to AACGM-v2; too high\n");
hgt = 2500;
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A);
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
next();
#endif

#if (DEBUG > 1)
printf("TEST: geographic to AACGM-v2; trace high\n");
hgt = 7500;
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A|TRACE);
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
next();
#endif

#if (DEBUG > 1)
printf("TEST: geographic to AACGM-v2; coefficient high\n");
hgt = 7500;
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A|BADIDEA);
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
next();
#endif

line('-',80);
CR;
printf("Testing MLT\n");
line('-',80);
CR;

lat = 77.;
lat = 37.;
lon = -88.;
hgt = 300.;

yr = 2003;
mo = 5;
dy = 17;
hr = 7;
mt = 53;
sc = 16;

/* compute AACGM lat/lon */
AACGM_v2_SetDateTime(yr, mo, dy, hr, mt, sc);
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A|TRACE);
mlt_t = MLTConvertYMDHMS_v2(yr,mo,dy,hr,mt,sc,mlon);
printf("      GLAT       GLON        HEIGHT       MLAT       MLON       MLT\n");
printf("TRACE %lf  %lf  %lf  %lf  %lf  %lf", lat,lon,hgt, mlat,mlon,mlt_t);
printf("\n");

err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A);
mlt_c = MLTConvertYMDHMS_v2(yr,mo,dy,hr,mt,sc,mlon);
printf("COEFF %lf  %lf  %lf  %lf  %lf  %lf", lat,lon,hgt, mlat,mlon,mlt_c);
printf("\n\n");

npts = 20;
printf("\n");
printf("Array:\n");
for (k=0; k<npts; k++) {
  lat = 45.;
  lon = k;
  hgt = 150.;

  err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A|TRACE);
  mlt_t = MLTConvertYMDHMS_v2(yr,mo,dy,hr,mt,sc,mlon);
  printf("      %7.4lf %8.4lf  %10.4lf  %10.4lf  %10.4lf  %10.4lf\n",
                lat,lon,hgt, mlat,mlon,mlt_t);
}
printf("\n\n");

return (0);
}

void next(void)
{
  char ch;

  printf("Press Enter to continue ");
  do {
    scanf("%c", &ch);
  } while (ch != '\n');

  /*  printf("\n\n"); AGB: Fixed C++ style commenting */
  printf("\f");
}

void line(char ch, int n)
{
  int k;

  for (k=0;k<n;k++) printf("%c", ch);
  printf("\n");
}

