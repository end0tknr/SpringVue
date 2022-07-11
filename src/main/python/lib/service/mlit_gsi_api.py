#!python
# -*- coding: utf-8 -*-

import appbase
import json
import time
import urllib.request
logger = logger = appbase.AppBase().get_logger()

geocode_api = "https://msearch.gsi.go.jp/address-search/AddressSearch"

# 国交省 国土地理院が提供するAPI
class MlitGsiApiService(appbase.AppBase):

    def __init__(self):
        pass

    #例 https://msearch.gsi.go.jp/address-search/AddressSearch?q=東京都渋谷駅
    def conv_addr_to_lng_lat(self,address_str):
        conf = self.get_conf()
        
        req_params = {}
        req_params["q"]  = address_str
        req_params_str = urllib.parse.urlencode(req_params)

        req_url = geocode_api +"?"+ req_params_str
        req = urllib.request.Request(req_url)
        try:
            res = urllib.request.urlopen(req)
        except Exception as e:
            logger.error(e)
            return None

        content_str = res.read()
        res.close()
    
        # response 例
        #[{"geometry":{"coordinates":[139.697723,35.66367],"type":"Point"},
        #  "type":"Feature",
        #  "properties":{"addressCode":"","title":"東京都渋谷区"}}]
        try:
            content = json.loads(content_str)
        except Exception as e:
            logger.error(e)
            logger.error(content_str)
            return None

        if len(content) == 0:
            logger.error("fail conv from json "+content_str.decode() )
            return None

        ret_data = {}
        ret_data["lng"]  = content[0]["geometry"]["coordinates"][0] #経度
        ret_data["lat"]  = content[0]["geometry"]["coordinates"][1] #緯度
        ret_data["title"]= content[0]["properties"]["title"]
        return ret_data
    
