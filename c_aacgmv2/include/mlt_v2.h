
#ifndef _MLT_v2_H
#define _MLT_v2_H

double MLTConvert_v2(int yr, int mo, int dy, int hr, int mt ,int sc,
                      double mlon);
double inv_MLTConvert_v2(int yr, int mo, int dy, int hr, int mt ,int sc,
                      double mlt);
double MLTConvertYMDHMS_v2(int yr,int mo,int dy,int hr,int mt,int sc,
                      double mlon);
double inv_MLTConvertYMDHMS_v2(int yr,int mo,int dy,int hr,int mt,int sc,
                      double mlt);
double MLTConvertYrsec_v2(int yr,int yrsec, double mlon);
double inv_MLTConvertYrsec_v2(int yr,int yrsec, double mlt);
double MLTConvertEpoch_v2(double epoch, double mlon);
double inv_MLTConvertEpoch_v2(double epoch, double mlt);

#endif

