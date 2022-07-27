#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files?page=1&toukei=00200521&tstat=000001136464&tclass1=000001136472
# 8-1 住宅の建て方別一般世帯数－町丁・字等

from service.city import CityService
from util.db      import Db
import appbase
import csv
import io
import re
import service.kokusei_population_h

data_name = "住宅の建て方別一般世帯数－町丁・字等"
pkey_cols  = ["pref","city","town"]
other_cols = ["total","detached_house","tenement_houses","apartment"]

logger = appbase.AppBase().get_logger()

class KokuseiPopulationH08Service(
        service.kokusei_population_h.KokuseiPopulationHService ):

    def __init__(self):
        pass

    def download_save_data_src(self,pref_url):
        logger.info(pref_url)

        pref_html = self.get_http_requests( pref_url )
        download_url = self.get_download_url(pref_html,data_name)
        csv_content = self.get_http_requests( download_url )
        ret_datas = self.load_csv_content( csv_content )
        
        util_db = Db()
        util_db.bulk_upsert("kokusei_population_h08",
                            pkey_cols,
                            pkey_cols + other_cols,
                            other_cols,
                            ret_datas )
            
    def load_csv_content( self, csv_content ):
        city_service = CityService()
        ret_datas_tmp = {}

        f = io.StringIO()
        f.write( csv_content.decode(encoding='cp932') )
        f.seek(0)
        for cols in csv.reader( f ):

            pref_name = cols[7]
            city_name = cols[8]
            town_name = cols[9]
            if not pref_name or \
               not city_name or \
               not town_name or \
               cols[10]: # 丁番地 lebelは db登録対象外
                continue

            # 「宮ケ丘（番地）」のような()付は db登録対象外
            if "（" in town_name:
                continue

            city_def = city_service.find_def_by_pref_city(pref_name,
                                                          city_name)
            if not city_def:
                continue

            pref_city_town = "\t".join([pref_name,city_name,town_name])

            if not pref_city_town in ret_datas_tmp:
                ret_datas_tmp[pref_city_town] = {}
                for col_name in other_cols:
                    ret_datas_tmp[pref_city_town][col_name] = 0

            i = 0
            for col_no in [11,14,15,16,]:
                if cols[col_no] in ["-","X"]:
                    cols[col_no] = 0
                else:
                    cols[col_no] = int( cols[col_no] )

                col_name = other_cols[i]
                ret_datas_tmp[pref_city_town][col_name] += cols[col_no]
                i += 1
            
        return self.conv_hash_to_list(ret_datas_tmp)
