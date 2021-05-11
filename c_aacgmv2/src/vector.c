/* ----------------------------------------------------------------------------
; AACGM spherical to vector transformation
;
; Convert velocity vectors in spherical coords into AACGMV2 magnetic coords
;
; Author:
! 201202 - C.L. Waters (CLW), Centre for Space Physics, University of Newcastle
!          Australia: Original written in Fortran and implemented through a
;          C wrapper on the AACGMV2 library.
!
! Modifications:
!
; 202105 - AGB translated Fortran code
; --------------------------------------------------------------------------- */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "aacgmlib_v2.h"
#include "igrflib.h"
#include "genmag.h"

#define DEBUG 0

/**
 * @brief Convert vectors from geocentric spherical coordinates to AACGMV2.
 *        Returns an error code, which is zero upon success.
 *
 * @param[in] dataGEO
 *
 * @param[out] aacgm_clat_rad
 *             aacgm_lon_rad
 *             dbthet_aacgm_th
 *             dbphi_aacgm_th
 *             dbthet_aacgm_ph
 *             dbphi_aacgm_ph
 **/
void geosph_to_aacgmvec(struct ampData *dataGEO, double *aacgm_clat_rad,
			double *aacgm_lon_rad, double *dbthet_aacgm_th,
			double *dbphi_aacgm_th, double *dbthet_aacgm_ph,
			double *dbphi_aacgm_ph)
{
  int i, s, flg, np;
  
  double geo_r_km, geo_clat_rad, geo_lon_rad, geo_db_thet, geo_db_phi;
  double geo_lat_deg, geo_lon_deg, mlat, mlon, mrad, mclat_rad, mlon_rad;
  double vx, vy, vz, br, bth, bph, rg_th, glat_th, cglat_th, glon_th;
 
  double geo_xyz[3], geo_xyz_th[3], geo_xyz_ph[3], geo_rtp_th[3];
  double geo_rtp_ph[3], aacgm_xyz[3], aacgm_xyz_th[3], aacgm_xyz_ph[3];
  double mxyz_r[3], mxyz_ruv[3], mxyz_th[3], mxyz_thuv[3], mxyz_ph[3];
  double mxyz_phuv[3], mxyz_ph_gth[3], mxyz_th_gph[3], mvec_th[3], mvec_ph[3];

  char err_msg[50];

  sprintf(err_msg, "ERR: AACGM conv error in geosph_to_aacgmvec");

  /* FIX: DETERMINE WHAT THIS STRUCTURE IS LIKE AND GET THE SIZE */
  np = size(dataGEO);

  /* Rotate vectors from GEO to AACGM */
  for(i=0; i<np; i++)
    {
      /* FIX: R, T, P, bT, bP are not defined */
      geo_r_km = dataGEO[i].R;
      geo_clat_rad = dataGEO[i].T;
      geo_lon_rad = dataGEO[i].P;
      geo_db_thet = dataGEO[i].bT;
      geo_db_phi = dataGEO[i].bP;

      /* Geographic spherical coordinates to geographic cartesian */
      sphcar_08(geo_r_km, geo_clat_rad, geo_lon_rad, geo_xyz[1], geo_xyz[2],
		geo_xyz[3], 1);
 
      /* Geographic spherical to AACGMV2 coords */
      geo_lat_deg = 90.0 - geo_clat_rad * 180.0 / M_PI;
      geo_lon_deg = geo_lon_rad * 180.0 / M_PI;
      /* aacgm_hgt = rsat/1000.0 */
      flg = 0;
 
      s = AACGM_v2_Convert(geo_lat_deg, geo_lon_deg, hS_km, mlat, mlon, mrad,
			   flg);
 
      if(s != 0)
	{
	  printf("%s\nErr in AACGM_v2_Convert: GEO->AACGM\n", err_msg);
	  printf("Inputs were: %f %f %f\n", geo_lat_deg, geo_lon_deg, hS_km);
	  return(1500);
	}

      if(mlon < 0.0) mlon += 360.0;

      aacgm_lon_rad[i] = mlon * M_PI / 180.0;
 
      /* AACGM_spherical to x,y,z */
      aacgm_clat_rad[i] = (90.0 - mlat) * M_PI / 180.0;
      sphcar_08(geo_r_km, aacgm_clat_rad[i], aacgm_lon_rad[i], aacgm_xyz[1],
		aacgm_xyz[2], aacgm_xyz[3], 1);
 
      /* - - - - - - - - - del_th in GEO - - - - - - - - - - */
      br  = 0.0;
      bth = 1.0;
      bph = 0.0;

      bspcar_08(geo_clat_rad, geo_lon_rad, br, bth, bph, vx, vy, vz);

      geo_xyz_th[1] = geo_xyz[1] + vx;
      geo_xyz_th[2] = geo_xyz[2] + vy;
      geo_xyz_th[3] = geo_xyz[3] + vz;
 
      /* Conv x,y,z to spherical */
      sphcar_08(geo_rtp_th[1], geo_rtp_th[2], geo_rtp_th[3], geo_xyz_th[1],
		geo_xyz_th[2], geo_xyz_th[3], -1);
 
      geo_rtp_th[2] = 90.0 - geo_rtp_th[2] * 180.0 / M_PI;
      geo_rtp_th[3] = geo_rtp_th[3] * 180.0 / M_PI;

      /* Convert to AACGM (from GEO_th) */
      flg = 0;
      s = AACGM_v2_Convert(geo_rtp_th[2], geo_rtp_th[3], hS_km, mlat, mlon,
			   mrad, flg);
 
      if(s != 0)
	{
	  printf("%s\nErr in AACGM_v2_Convert: GEO->AACGM\n", err_msg);
	  printf("Inputs were: %f %f %f\n", geo_rtp_th[2], geo_rtp_th[3],
		 hS_km);
	  return(1501);
	}

      mclat_rad = (90.0 - mlat) * M_PI / 180.0;
      if(mlon < 0.0) mlon += 360.0;
      mlon_rad = mlon * M_PI / 180.0;

      /* Get x,y,z coords of AACGM + dthet */
      sphcar_08(geo_r_km, mclat_rad, mlon_rad, aacgm_xyz_th[1], aacgm_xyz_th[2],
		aacgm_xyz_th[3], 1);

      /* - - - - -  - del_phi in GEO  - - - - - - - - - - */
      br  = 0.0;
      bth = 0.0;
      bph = 1.0;

      bspcar_08(geo_clat_rad, geo_lon_rad, br, bth, bph, vx, vy, vz);

      geo_xyz_ph[1] = geo_xyz[1] + vx;
      geo_xyz_ph[2] = geo_xyz[2] + vy;
      geo_xyz_ph[3] = geo_xyz[3] + vz;
 
      /* Conv x,y,z to spherical */
      sphcar_08(geo_rtp_ph[1], geo_rtp_ph[2], geo_rtp_ph[3], geo_xyz_ph[1],
		geo_xyz_ph[2], geo_xyz_ph[3], -1);
 
      geo_rtp_ph[2] = 90.0 - geo_rtp_ph[2] * 180.0 / M_PI;
      geo_rtp_ph[3] = geo_rtp_ph[3] * 180.0 / M_PI;
 
      /* convert to AACGM (from GEO_ph) */
      flg = 0;
      s = AACGM_v2_Convert(geo_rtp_ph[2], geo_rtp_ph[3], hS_km, mlat, mlon,
			   mrad, flg);
 
      if(s != 0)
	{
	  printf("%s\nErr in AACGM_v2_Convert: GEO->AACGM\n", err_msg);
	  printf("Inputs were: %f %f %f\n", geo_rtp_ph[2], geo_rtp_ph[3],
		 hS_km);
	  return(1502);
	}

      mclat_rad = (90.0 - mlat) * M_PI / 180.0;
      if(mlon < 0.0) mlon += 360.0;
      mlon_rad = mlon * M_PI / 180.0;
 
      /* Get x,y,z coords of AACGM + dthet */
      sphcar_08(geo_r_km, mclat_rad, mlon_rad, aacgm_xyz_ph[1], aacgm_xyz_ph[2],
		aacgm_xyz_ph[3], 1);

      /* - - - - - - Finalize the conversion - - - - - - - - - - */
      /* calc AACGM radial unit vector */
      mxyz_ruv = norm_vec(aacgm_xyz);

      /* calc AACGM(x,y,z) unit vector for a GEO dth shift */
      mxyz_th = aacgm_xyz_th - aacgm_xyz;
      mxyz_thuv = norm_vec(mxyz_th);

      /* calc AACGM(x,y,z) unit vector for a GEO dph shift */
      mxyz_ph = aacgm_xyz_ph - aacgm_xyz;
      mxyz_phuv = norm_vec(mxyz_ph);

      /* calc cross products */
      mxyz_ph_gth = cross_p(mxyz_ruv, mxyz_thuv);
      
      /* For a GEO dth shift -> AACGM dth */
      bcarsp_08(aacgm_xyz[1], aacgm_xyz[2], aacgm_xyz[3], mxyz_thuv[1],
		mxyz_thuv[2], mxyz_thuv[3], mvec_th[1], mvec_th[2], mvec_th[3]);

      /* For a GEO dth shift -> AACGM dph */
      bcarsp_08(aacgm_xyz[1], aacgm_xyz[2], aacgm_xyz[3], mxyz_ph_gth[1],
		mxyz_ph_gth[2], mxyz_ph_gth[3], mvec_ph[1], mvec_ph[2],
		mvec_ph[3]);

      dbthet_aacgm_th[i] = geo_db_thet * mvec_th[2] + geo_db_phi * mvec_ph[2];
      dbphi_aacgm_th[i]  = geo_db_thet * mvec_th[3] + geo_db_phi * mvec_ph[3];

      /* Now do the PHI components.              */
      /* Start by calculating the cross products */
      mxyz_th_gph = cross_p(mxyz_phuv, mxyz_ruv);

      /* For a GEO dph shift -> AACGM dth */
      bcarsp_08(aacgm_xyz[1], aacgm_xyz[2], aacgm_xyz[3], mxyz_th_gph[1],
		mxyz_th_gph[2], mxyz_th_gph[3], mvec_th[1], mvec_th[2],
		mvec_th[3]);

      /* For a GEO dph shift -> AACGM dph */
      bcarsp_08(aacgm_xyz[1], aacgm_xyz[2], aacgm_xyz[3], mxyz_phuv[1],
		mxyz_phuv[2], mxyz_phuv[3], mvec_ph[1], mvec_ph[2], mvec_ph[3]);

      dbthet_aacgm_ph[i] = geo_db_thet * mvec_th[2] + geo_db_phi * mvec_ph[2];
      dbphi_aacgm_ph[i]  = geo_db_thet * mvec_th[3] + geo_db_phi * mvec_ph[3];
    }

  return(0);
}
