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
from util.db            import Db

def main():
    # gis_service = GisService()
    # data_names = [
    #     #"gis_gyosei_kuiki",
    #     #"gis_chika_koji",
    #     #"gis_chika",
    #     #        "gis_youto_chiiki",
    #     #"gis_tochi_riyo",
    #     #"gis_tochi_riyo_saibun",
    #     "gis_tochi_riyo_shousai",
    # ]
    # for data_name in data_names:
    #     data_urls = gis_service.find_data_urls(data_name)
    #     print( data_urls )

    # gmap_service = GoogleMapService()
    # lng_lat = gmap_service.conv_addr_to_lng_lat("国分寺市西町2-7-74")
    # print( lng_lat )

    # gis_service = GisService()
    # gis_mesh_codes = ['684','6848','5439','543943','54394324','5439432400']
    # for mesh_code in gis_mesh_codes:
    #     lat_lng = gmap_service.conv_gis_mesh_code_to_lat_lng(mesh_code)
    #     if not lat_lng:
    #         continue
    #     print( lat_lng )
    #     addr = gmap_service.conv_lat_lng_to_addr(lat_lng['lat'],lat_lng['lng'])
    #     addr["mesh_code"] = mesh_code
    #     # gmap_service.add_latlan_addr_to_db(addr)

    # gmap_service = GoogleMapService()
    # gis_mesh_codes = ['684','6848','5439','543943','54394324','5439432400']
    # for mesh_code in gis_mesh_codes:
    #     lat_lng = gmap_service.get_latlan_from_db_by_mesh_code(mesh_code)
    #     if not lat_lng:
    #         continue
    #     print( lat_lng )

    gis_service = GisService()
    col_comments = gis_service.find_db_col_comment(
        'https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v3_0.html' )
    print( col_comments )

    db = Db()
    print( db.col_defs("gyosei_kuiki") )

    
    # zipcode_service = ZipcodeService()
    # zipcodes = zipcode_service.download_master()
    # print( zipcodes )
    
    # city_service = CityService()
    # cities = city_service.download_master()
    # print( cities )

    
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
    #     print(sqls)

    #     for sql in sqls:
    #         if i == 0:
    #             gis_service.drop_master_tbl("youto_chiiki")
    #             gis_service.create_master_tbl(sql["create"])
            
    #         gis_service.insert_master_tbl(sql["insert"])
    #         i += 1

    
if __name__ == '__main__':
    main()
    
