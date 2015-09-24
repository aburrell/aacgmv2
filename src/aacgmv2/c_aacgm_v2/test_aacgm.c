#include <stdio.h>
#include "aacgmlib_v2.h"

void next(void);

int main(void)
{
double lat,lon,hgt;
double h;
double rtp[3];
double mlat,mlon,r;
int err;
int year, month, day, hour, minute, second;

printf("AACGM-v2 Test Program\n\n");

/* compute AACGM-v2 lat/lon with no time specified */
printf("TEST: no date/time\n");
lat = 45.5;
lon = -23.5;
hgt = 1135.;
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A);
if (err == 0) {
	printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
	printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
	printf("\n\n");
}
next();

printf("TEST: Setting time to : %04d%02d%02d %02d%02d:%02d\n", 1850,1,22,0,0,0);
AACGM_v2_SetDateTime(1850, 1, 22, 0,0,0);	/* this should fail */
next();
printf("TEST: Setting time to : %04d%02d%02d %02d%02d:%02d\n", 1900,1,22,0,0,0);
AACGM_v2_SetDateTime(1900, 1, 22, 0,0,0);	/* this is valid */
next();
printf("TEST: Setting time to : %04d%02d%02d %02d%02d:%02d\n", 2020,1,22,0,0,0);
AACGM_v2_SetDateTime(2020, 1, 22, 0,0,0);	/* this shoudl fail */
next();
printf("TEST: Setting time to : %04d%02d%02d %02d%02d:%02d\n", 2019,1,22,0,0,0);
AACGM_v2_SetDateTime(2019, 1, 22, 0,0,0);	/* this is valid */
next();

year   = 2014;
month  = 3;
day    = 22;
hour   = 3;
minute = 11;
second = 0;
printf("TEST: Setting time to : %04d%02d%02d %02d%02d:%02d\n",
					year, month, day, hour, minute, second);

/* set date and time */
AACGM_v2_SetDateTime(year, month, day, hour, minute, second);

printf("TEST: geographic to AACGM-v2\n");
/* compute AACGM lat/lon */
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A);

printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
//printf("%lf %lf\n", fyear, fyear_old);
printf("\n\n");
next();

printf("TEST: AACGM-v2 to geographic\n");
/* do the inverse: A2G */
err = AACGM_v2_Convert(mlat,mlon,hgt, &lat,&lon, &r, A2G);

printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("\n\n");
next();

/* compare tracing to coefficients */
lat = 45.5;
lon = -23.5;
hgt = 150.;

/* set date and time */
AACGM_v2_SetDateTime(2018,1,1,0,0,0);

printf("TEST: geographic to AACGM-v2; coefficients\n");
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A);
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
next();

printf("TEST: geographic to AACGM-v2; tracing\n");
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A|TRACE);
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
next();

printf("TEST: geographic to AACGM-v2; too high\n");
hgt = 2500;
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A);
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
next();

printf("TEST: geographic to AACGM-v2; trace high\n");
hgt = 7500;
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A|TRACE);
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
next();

printf("TEST: geographic to AACGM-v2; coefficient high\n");
hgt = 7500;
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A|BADIDEA);
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
next();

printf("TEST: geographic to AACGM-v2; trace and back\n");
hgt = 0;
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A|TRACE);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
err = AACGM_v2_Convert(mlat,mlon,hgt, &lat,&lon, &r, A2G|TRACE);
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);

/* the proper altitude in geocentric coordinates is given by: */
geod2geoc(lat,lon,hgt, rtp);
h = (rtp[0]-1.d)*RE;
err = AACGM_v2_Convert(mlat,mlon,h, &lat,&lon, &r, A2G|TRACE);
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);

next();

lat = 45.5;
lon = -23.5;

printf("TEST: geographic to AACGM-v2; coeff and back\n");
hgt = 0;
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
err = AACGM_v2_Convert(mlat,mlon,hgt, &lat,&lon, &r, A2G);
printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
next();

return (0);

/* pick a different year */
year   = 1997;
AACGM_v2_SetDateTime(year, month, day, hour, minute, second);

err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A);

printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
//printf("%lf %lf\n", fyear, fyear_old);
printf("\n\n");

/* pick a different lat/lon; should not need to do any interpolations */
lat = 65.5;
lon = 93.5;
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A);

printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
//printf("%lf %lf\n", fyear, fyear_old);
printf("\n\n");

/* pick a different height; should only need to do height interpolation */
hgt = 0.;
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A);

printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
printf("\n\n");

/* do another lat/lon; no interpolations */
lat = 75.5;
lon = 73.5;
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A);

printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
printf("\n\n");

/* pick another year; should require loading new coeffs and both interps */
year   = 2004;
month  = 3;
day    = 22;
hour   = 3;
minute = 11;
second = 0;

AACGM_v2_SetDateTime(year, month, day, hour, minute, second);

err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, G2A);

printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
printf("\n\n");
}

void next(void)
{
	char ch;

	printf("Press Enter to continue ");
	do {
		scanf("%c", &ch);
	} while (ch != '\n');

//	printf("\n\n");
	printf("\f");
}

