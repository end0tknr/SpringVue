#!python
# -*- coding: utf-8 -*-

from service.city      import CityService
import re
import service.gis_chika_koji

logger = None

class GisChikaService(service.gis_chika_koji.GisChikaKojiService):

    def __init__(self):
        global logger
        logger = self.get_logger()
        

    def modify_pref_cities(self):
        logger.info("start")
        
        city_service = CityService()
        org_datas = self.get_pref_cities_for_modiry()
        for org_data in org_datas:
            new_data = city_service.parse_pref_city(org_data["org_address"])
            self.save_pref_cities(org_data["gid"],new_data[0],new_data[1])
            
    def save_pref_cities(self,gid,pref,city):
        sql = """
UPDATE gis_chika
SET pref=%s, city=%s
WHERE gid=%s
"""
        sql_args = (pref,city,gid)
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:
                try:
                    db_cur.execute(sql,sql_args)
                except Exception as e:
                    logger.error(e)
                    logger.error(sql)
                    return False
        return True

            
    def get_pref_cities_for_modiry(self):

        sql = """
SELECT
  gid,
  l02_022 as org_address
FROM gis_chika
WHERE pref is null or city is null;
"""
        ret_data = []
        
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:
                try:
                    db_cur.execute(sql)
                except Exception as e:
                    logger.error(e)
                    logger.error(sql)
                    return []
                
                for ret_row in  db_cur.fetchall():
                    ret_row = dict( ret_row )
                    ret_row["org_address"] = \
                        ret_row["org_address"].replace("　","").replace(" ","")
                    ret_data.append( ret_row )
                
        return ret_data
