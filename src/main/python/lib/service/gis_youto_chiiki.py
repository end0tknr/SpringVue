#!python
# -*- coding: utf-8 -*-

from service.city      import CityService
from service.googlemap import GoogleMapService
import re
import service.gis

logger = None

class GisYoutoChiikiService(service.gis.GisService):

    def __init__(self):
        global logger
        logger = self.get_logger()
        

    # 例 横浜市 -> 横浜市青葉区
    def modify_seirei_city_names(self):
        logger.info("start")
        
        city_service = CityService()
        seirei_cities = city_service.get_seirei_cities()
        for seirei_city in seirei_cities:
            logger.info(seirei_city["pref"] + seirei_city["city"] )
            org_cities = self.get_seirei_cities_for_modify(seirei_city["pref"],
                                                           seirei_city["city"] )
            gmap_service = GoogleMapService()
            new_cities = gmap_service.conv_lng_lat_to_addrs(org_cities)
            for new_city in new_cities:
                self.modify_seirei_city_name(new_city)
                
                
    def modify_seirei_city_name(self, new_city):
        
        sql = """
UPDATE gis_youto_chiiki SET a29_003=%s WHERE gid=%s
"""
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:
                sql_args = ( new_city["city"],
                             new_city["gid"])
                try:
                    db_cur.execute(sql , sql_args )
                    db_conn.commit()
                except Exception as e:
                    logger.error(e)
                    logger.error(sql)
                    return False
        return True

        
    def get_seirei_cities_for_modify(self,pref, city):

        ret_data = []
        sql = """
SELECT
  gid,
  a29_002 as pref,
  a29_003 as city,
  ST_AsText(ST_Centroid(geom)) as lng_lat
FROM gis_youto_chiiki
WHERE a29_002=%s AND a29_003=%s
"""
        re_compile = re.compile("(\d+\.\d+) (\d+\.\d+)")
        
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:
                try:
                    db_cur.execute(sql, (pref,city) )
                except Exception as e:
                    logger.error(e)
                    logger.error(sql)
                    return []
                
                for ret_row in  db_cur.fetchall():
                    ret_row = dict( ret_row )
                    
                    re_result = re_compile.search( str(ret_row["lng_lat"]))
                    if not re_result:
                        logger.error("fail parse")
                        logger.error(ret_row)
                        continue
                    ret_row["lng"] = re_result.group(1)
                    ret_row["lat"] = re_result.group(2)
                    ret_data.append( ret_row )
        return ret_data


    def get_group_by_city(self):
        sql = """
select
 a29_002 as pref,
 a29_003 as city,
 a29_005 as usage,
 round( sum(ST_Area(geom) * 10^10) ) as m2
from  gis_youto_chiiki
group by pref,city,usage
"""
        ret_data_tmp = {}
        usages = {}
        
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
                    pref_city = "%s\t%s" %(ret_row["pref"],ret_row["city"])
                    if not pref_city in ret_data_tmp:
                        ret_data_tmp[pref_city] = {"pref":ret_row["pref"],
                                                   "city":ret_row["city"]}

                    usage = ret_row["usage"]
                    ret_data_tmp[pref_city][usage] = ret_row["m2"]
                    if not usage in usages:
                        usages[usage] = 1
            
            usages = list(usages.keys())
            usages.sort()
        
            return ret_data_tmp.values()
            #return ret_data_tmp.values(), usages
    
