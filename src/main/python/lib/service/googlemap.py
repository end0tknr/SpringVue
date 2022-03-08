#!python
# -*- coding: utf-8 -*-

import appbase
import json
import urllib.parse
import urllib.request

geocode_api = "https://maps.google.com/maps/api/geocode/json"


class GoogleMapService(appbase.AppBase):
    
    def __init__(self):
        pass

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
            res = urllib.request.urlopen(req)
        except:
            return None

        content_str = res.read()
        res.close()
    
        content = json.loads(content_str)
        if content['status'] != "OK":
            return None

        ret_data = content["results"][0]["geometry"]["location"]
        ret_data["formatted_address"] = content["results"][0]["formatted_address"]
        
        return ret_data
        
