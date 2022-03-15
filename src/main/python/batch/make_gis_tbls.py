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
    gis_service = GisService()
    util_db = Db()
    
    data_names = gis_service.get_data_names()
    for data_name in data_names:
        print(data_name)
        if data_name != 'gis_youto_chiiki':
            continue

        index_page_url = gis_service.get_index_page_url(data_name)
        print( index_page_url )
        
        data_urls = gis_service.find_data_urls(index_page_url)
        data_url = data_urls[-1] # 最終行のものが、最新のはず
        #print( data_url )

        sqls = gis_service.download_master(data_url["url"], data_name )
        print( sqls[0]["create"] )

        #result = gis_service.create_master_tbl( sqls[0]["create"] )
        #print( result )

        tbl_comment = gis_service.find_db_tbl_comment(index_page_url)
        print("HOGE:", tbl_comment )
        continue
    
        col_defs = util_db.col_defs(data_name)
        col_names = []
        for col_def in col_defs:
            col_names.append( col_def["column_name"] )
            
        col_comments = gis_service.find_db_col_comment(index_page_url)
        for col_name, comment in  col_comments.items():
            if not col_name in col_names:
                continue

            result = util_db.save_col_comment(data_name,col_name,comment)
            print(data_name,col_name,comment,result)
        
        
if __name__ == '__main__':
    main()
    
