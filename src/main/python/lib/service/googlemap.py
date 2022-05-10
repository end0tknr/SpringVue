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
    
    def parse_address_components(self, components ):

        components = list( reversed(components) )
        ret_vals = []
        found_jp = None
        for component in components:
            
            if found_jp:
                ret_vals.append( component["long_name"] )
                continue
            
            if component["long_name"] == "日本":
                found_jp = True

        return ret_vals

    # browser(selenium)の起動がある為、複数の座標をまとめての変換がお得
    def conv_lng_lat_to_addrs(self,lng_lats):
        browser = self.get_browser()
        re_compile = re.compile(" (.+)、(.+)")
        
        for lng_lat in lng_lats:
            req_url = "https://www.google.co.jp/maps/search/%s,%s" \
                % (lng_lat["lat"],lng_lat["lng"])
            browser.get(req_url)
            browser.save_screenshot("/home/end0tknr/tmp/screenshot_hoge.png")

            div_elms  = browser.find_elements_by_css_selector("div.LCF4w")
            lng_lat["address_other"] = div_elms[0].text
            re_result = re_compile.search( div_elms[1].text )
            if not re_result:
                lng_lat["pref"] = "?"
                lng_lat["city"] = "?"
                logger.error("%s,%s -> %s %s %s" %
                             (lng_lat["lat"],lng_lat["lng"],
                              lng_lat["pref"],lng_lat["city"],lng_lat["address_other"]))
                continue

            lng_lat["pref"] = re_result.group(2)
            lng_lat["city"] = re_result.group(1)
            
            if not lng_lat["pref"][-1] in ["都","道","府","県"] or \
               not lng_lat["city"][-1] in ["市","区","町","村"] :
                
                lng_lat["pref"] = "?"
                lng_lat["city"] = "?"
                
                logger.warning("%s,%s -> %s %s %s" %
                               (lng_lat["lat"],lng_lat["lng"],
                                lng_lat["pref"],lng_lat["city"],lng_lat["address_other"]))
                continue
            
            logger.info("%s,%s -> %s %s %s" %
                        (lng_lat["lat"],lng_lat["lng"],
                         lng_lat["pref"],lng_lat["city"],lng_lat["address_other"]))
            
        return lng_lats

    
    def conv_lng_lat_to_addr(self,lng,lat):
        conf = self.get_conf()

        req_params = {}
        req_params["key"]      = conf["common"]["google_map_api_key"]
        req_params["language"] = "ja"
        req_params["latlng"]  = ",".join([str(lat),str(lng)])
        req_params_str = urllib.parse.urlencode(req_params)

        req_url = geocode_api +"?"+ req_params_str
        #print( req_url )

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
        
        ret_data["address_components"] = \
            self.parse_address_components(
                content["results"][0]["address_components"] )

        return ret_data
        
