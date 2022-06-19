#!python
# -*- coding: utf-8 -*-

from service.city      import CityService
import service.gis
import re
import sys

logger = None

class GisGyoseiKuikiService(service.gis.GisService):

    def __init__(self):
        global logger
        logger = self.get_logger()
        
    def calc_bounding_box(self,pref,city):
        city_service = CityService()
        
        if city_service.is_seirei_city(city):
            re_compile = re.compile("(.+市)(.+区)")
            re_result = re_compile.search(city)
            if re_result:
                return self.calc_bounding_box_sub_1(pref,
                                                    re_result.group(1),
                                                    re_result.group(2))
            return self.calc_bounding_box_sub_1(pref,
                                                city,
                                                "")
        return self.calc_bounding_box_sub_2(pref,city)

    def conv_coords_to_geometory(self,coords):
        geom_text = \
            "POLYGON((%f %f,%f %f,%f %f,%f %f,%f %f))" % \
            (coords["min_x"],coords["max_y"],
             coords["max_x"],coords["max_y"],
             coords["max_x"],coords["min_y"],
             coords["min_x"],coords["min_y"],
             coords["min_x"],coords["max_y"])
        return geom_text
        
    def calc_bounding_box_sub_1(self,pref,city_1,city_2):

        sql = """
SELECT min(ST_XMin(geom)) as min_x,
       max(ST_XMax(geom)) as max_x,
       min(ST_YMin(geom)) as min_y,
       max(ST_YMax(geom)) as max_y
FROM gis_gyosei_kuiki
WHERE n03_001=%s AND n03_003=%s AND n03_004=%s
"""
        ret_data = []
        db_conn = self.db_connect()
        
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute(sql,(pref,city_1,city_2))
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return None
            
            ret_rows = db_cur.fetchall()
            ret_row = dict( ret_rows[0] )
        return self.conv_coords_to_geometory(ret_row)

    def calc_bounding_box_sub_2(self,pref,city):

        sql = """
SELECT min(ST_XMin(geom)) as min_x,
       max(ST_XMax(geom)) as max_x,
       min(ST_YMin(geom)) as min_y,
       max(ST_YMax(geom)) as max_y
FROM gis_gyosei_kuiki
WHERE n03_001=%s AND n03_004=%s
"""
        ret_data = []
        db_conn = self.db_connect()
        
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute(sql,(pref,city))
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return None
            
            ret_rows = db_cur.fetchall()
            ret_row = dict( ret_rows[0] )
        return self.conv_coords_to_geometory(ret_row)
    
    def find_cities_by_bouding_box(self,geom_polygon):

        sql = """
SELECT
  t1.n03_001 as pref,
  t1.n03_003 as city_1,
  t1.n03_004 as city_2
FROM gis_gyosei_kuiki t1
WHERE ST_Distance(t1.geom, %s::GEOMETRY) = 0
GROUP BY t1.n03_001, t1.n03_003, t1.n03_004
"""
        ret_data = []
        city_service = CityService()
        db_conn = self.db_connect()
        is_found = {}
        
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute(sql,(geom_polygon,))
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                sys.exit()
                return []
                
            for ret_row in  db_cur.fetchall():
                ret_row = dict( ret_row )
                if city_service.is_seirei_city(ret_row["city_1"]):
                    found_city = ret_row["city_1"]+ret_row["city_2"]
                else:
                    found_city = ret_row["city_2"]
                    
                found_pref_city = ret_row["pref"] + "\t" + found_city
                if found_pref_city in is_found:
                    continue
                is_found[found_pref_city] = 1
                    
                ret_data.append( {"pref":ret_row["pref"], "city":found_city} )
                
        return ret_data
