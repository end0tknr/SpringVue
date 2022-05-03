#!python
# -*- coding: utf-8 -*-

import appbase
import json
import re
import time
import urllib.parse
import urllib.request

geocode_api = "https://maps.google.com/maps/api/geocode/json"
logger = None

class GoogleMapService(appbase.AppBase):
    
    def __init__(self):
        global logger
        logger = self.get_logger()

    def load_addr_to_lng_lat(self,lng, lat):
        sql = "select * from gmap_latlng_addr where lng=%s and lat=%s"
        sql = sql % (lng,lat)
        
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:
                db_cur.execute(sql)
                rows = db_cur.fetchall()
                db_cur.close()

                if len(rows)==0:
                    return None

                return dict( rows[0] )
        return None
        
    def save_addr_info(self, addr_info):
        
        sql = """
INSERT INTO gmap_latlng_addr (lng,lat,zip_code,address)
VALUES (%s,%s,%s,%s)
"""
        values = ( round(addr_info["lng"],4),
                   round(addr_info["lat"],4),
                   addr_info["zip_code"],
                   addr_info["formatted_address"] )

        with self.db_connect()as db_conn:
            with self.db_cursor(db_conn) as db_cur:

                try:
                    db_cur.execute(sql, values )
                    db_conn.commit()
                    db_cur.close()
                except Exception as e:
                    logger.error(e)
                    logger.error(values)
                    return False
        
        return True
        
        
    #例 https://maps.google.com/maps/api/geocode/json?address=渋谷&key=ないしょ
    def conv_addr_to_lng_lat(self,address_str):
        conf = self.get_conf()
        
        req_params = {}
        req_params["key"]      = conf["common"]["google_map_api_key"]
        req_params["language"] = "ja"
        req_params["address"]  = address_str
        req_params_str = urllib.parse.urlencode(req_params)

        req_url = geocode_api +"?"+ req_params_str
        req = urllib.request.Request(req_url)
        try:
            time.sleep(1)
            res = urllib.request.urlopen(req)
        except Exception as e:
            logger.error(e)
            return None

        content_str = res.read()
        res.close()
    
        try:
            content = json.loads(content_str)
        except Exception as e:
            logger.error(e)
            logger.error(content_str)
            return False

        if content['status'] != "OK":
            logger.error("fail "+ req_params["address"] )
            logger.error(content)
            return None

        ret_data = content["results"][0]["geometry"]["location"]
        ret_data["lng"] = round(ret_data["lng"],4)
        ret_data["lat"] = round(ret_data["lat"],4)
        
        org_address = content["results"][0]["formatted_address"]
        ret_data.update( self.parse_formatted_address(org_address) )
        
        logger.debug(
            req_params["address"] + "->" +
            ret_data["lng"] + "," + ret_data["lng"] +
            ret_data["formatted_address"] )
        return ret_data
        
    def parse_formatted_address(self, org_addr ):
        re_result = re.compile("〒(\d\d\d-\d\d\d\d) ([^\s]+)").search(org_addr)
        if not re_result:
            return {"formatted_address":org_addr,"zip_code":None }

        return {"formatted_address":re_result.group(2),
                "zip_code":re_result.group(1) }
        
    def conv_lng_lat_to_addr(self,lng,lat):
        conf = self.get_conf()

        req_params = {}
        req_params["key"]      = conf["common"]["google_map_api_key"]
        req_params["language"] = "ja"
        req_params["latlng"]  = ",".join([str(lat),str(lng)])
        req_params_str = urllib.parse.urlencode(req_params)

        req_url = geocode_api +"?"+ req_params_str

        req = urllib.request.Request(req_url)
        try:
            time.sleep(1)
            res = urllib.request.urlopen(req)
        except Exception as e:
            logger.error(e)
            return None

        content_str = res.read()
        res.close()

        try:
            content = json.loads(content_str)
        except Exception as e:
            logger.error(e)
            logger.error(content_str)
            return False
        
        if content['status'] != "OK":
            logger.error("fail "+ req_params["latlng"] )
            logger.error(content)
            return None

        ret_data = content["results"][0]["geometry"]["location"]
        ret_data["lng"] = round(ret_data["lng"],4)
        ret_data["lat"] = round(ret_data["lat"],4)
        
        org_address = content["results"][0]["formatted_address"]
        ret_data.update( self.parse_formatted_address(org_address) )

        logger.debug(
            req_params["latlng"] + "->" + ret_data["formatted_address"] )

        return ret_data
        
