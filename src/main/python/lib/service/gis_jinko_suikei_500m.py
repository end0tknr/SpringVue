#!python
# -*- coding: utf-8 -*-

from service.city      import CityService
import appbase
import re
import service.gis
import sys

logger = appbase.AppBase().get_logger()

class GisJinkoSuikei500mService(service.gis.GisService):

    def __init__(self):
        pass
        

    def find_by_lnglat(self,lng,lat):
        
        if (not lng and not lat):
            logger.warning("lng lat is null")
            return {}
        
        sql ="""
SELECT *
FROM   gis_jinko_suikei_500m
WHERE  lng BETWEEN (%s-%s) AND (%s+%s) AND
       lat BETWEEN (%s-%s) AND (%s+%s)
ORDER BY ST_Distance(geom, ST_PointFromText(%s) )
LIMIT 1
"""
        db_conn = self.db_connect()
        limit_deg  = 0.01
        sql_args  = (lng, limit_deg, lng, limit_deg,
                     lat, limit_deg, lat, limit_deg,
                     "POINT(%s %s)" % (lng, lat) )
        
        years = ["2020","2030"]
        age_groups = {
            "pop_%s_20_24" : ["pt5"],
            "pop_%s_25_59" : ["pt6", "pt7", "pt8", "pt9", "pt10","pt11","pt12"],
            "pop_%s_60"    : ["pt13","pt14","pt15","pt16","pt17","pt18","pt19"] }

        ret_data = {}
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute(sql,sql_args)
            except Exception as e:
                logger.error(e)
                logger.error(sql + str(sql_args) )
                return {}

            ret_rows =  db_cur.fetchall()

            if len(ret_rows) == 0:
                return {}

            ret_row = dict( ret_rows[0] )
            ret_data = {"lng": ret_row["lng"], "lat": ret_row["lat"] }
            
            for year in years:
                for age_group, col_keys in age_groups.items():
                    age_group = age_group % (year,)
                    ret_data[age_group] = 0
                    
                    for col_key in col_keys:
                        col_key = col_key + "_" + year
                        ret_data[age_group] += ret_row[col_key]
                    ret_data[age_group] = int(ret_data[age_group])
                    
            return ret_data


