#!python
# -*- coding: utf-8 -*-

from service.newbuild               import NewBuildService
from util.db import Db
import appbase
import json
import re
import time

logger = appbase.AppBase().get_logger()

class TownService(appbase.AppBase):
    
    def __init__(self):
        pass

    def init_profiles(self):
        newbuild_service = NewBuildService()
        pref_city_towns = newbuild_service.get_all_town_names()
        # print( pref_city_towns )

        util_db = Db()
        util_db.bulk_upsert(
            "town_profile",
            ["pref","city","town"],
            ["pref","city","town"],
            pref_city_towns )
        return pref_city_towns

    def get_all(self):
        sql ="""
SELECT * from town_profile
ORDER BY pref,city,town
"""
        db_conn = self.db_connect()
        ret_datas = []
        
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute(sql)
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return []
            for ret_row in  db_cur.fetchall():
                ret_datas.append( dict( ret_row ))
                
        return ret_datas

    def save_lnglat(self, pref_city_town, longitude, latitude):
        sql ="""
UPDATE town_profile
SET    lng=%s, lat=%s
WHERE  pref=%s AND city=%s AND town=%s
"""
        sql_args = (longitude,
                    latitude,
                    pref_city_town["pref"],
                    pref_city_town["city"],
                    pref_city_town["town"] )

        db_conn = self.db_connect()
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute(sql,sql_args)
                db_conn.commit() 
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return False
            
        return True
        
        
        
    def calc_save_lnglat(self, pref_city_towns ):
        browser = self.get_browser()
        re_compile = re.compile("/@(\d+.\d+),(\d+\.\d+)\,\d+z/")

        max_retry = 10
        pos = 0
        for town in pref_city_towns:
            pos += 1
            
            if pos % 10 == 0:
                logger.info("%d / %d %s" % ( pos,len(pref_city_towns),town ) )
                # なんとなく browser再起動...
                # browser.close()
                # browser = self.get_browser()

                
            if "lng" in town  and "lat" in town  and town["lng"] and town["lat"]:
                continue
            
            
            pref_city_town = town["pref"] + town["city"] + town["town"]
            req_url = "https://www.google.com/maps/place/" + pref_city_town
            browser.get(req_url)
            i = 0
            longitude = None
            latitude  = None
            while i < max_retry:
                i += 1
                time.sleep(1)
                re_result = re_compile.search( browser.current_url )
                if not re_result:
                    continue
                longitude = re_result.group(1) # 緯度
                latitude  = re_result.group(2) # 経度
                self.save_lnglat(town, longitude, latitude )
                break

            if not longitude or not latitude:
                logger.error("fail calc lng lat for %s" % (pref_city_town,))

        browser.close()
