#!python3
# -*- coding: utf-8 -*-

import getopt
import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )

from service.city       import CityService
from service.gis        import GisService
from service.googlemap  import GoogleMapService
from service.zipcode    import ZipcodeService

def main():
    
    # zipcode_service = ZipcodeService()
    # zipcodes = zipcode_service.download_master()
    # print( zipcodes )
    
    # city_service = CityService()
    # cities = city_service.download_master()
    # print( cities )

    gmap_service = GoogleMapService()
    lng_lat = gmap_service.conv_addr_to_lng_lat("国分寺市西町2-7-74")
    print( lng_lat )
    
    # gis_service = GisService()
    # sqls = gis_service.download_master("gyosei_kuiki")

    # gis_service.drop_master_tbl("gyosei_kuiki")
    # gis_service.create_master_tbl(sqls["create"])
    # gis_service.insert_master_tbl(sqls["insert"])

    # gis_service = GisService()
    # url_infos = gis_service.scrape_download_urls(
    #     "https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-A29-v2_1.html" )
    # i = 0
    # for url_info in url_infos:
    #     print(url_info["url"])
    #     sqls = gis_service.download_master(url_info["url"],"youto_chiiki")

    #     for sql in sqls:
    #         if i == 0:
    #             gis_service.drop_master_tbl("youto_chiiki")
    #             gis_service.create_master_tbl(sql["create"])
            
    #         #gis_service.set_db_client_encoding("SJIS")
    #         gis_service.insert_master_tbl(sql["insert"])
    #         i += 1

    
if __name__ == '__main__':
    main()
    
