#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files?page=1&toukei=00200521&tstat=000001080615&tclass1=000001094495
# 3 年齢（5歳階級），男女別人口，総年齢及び平均年齢（外国人－特掲）－町丁・字等

from service.city import CityService
from util.db      import Db
import appbase
import csv
import io
import re
import service.kokusei2015_population_h

data_name = \
    "年齢（5歳階級），男女別人口，総年齢及び平均年齢（外国人－特掲）－町丁・字等"
pkey_cols = ["pref","city","town"]
other_cols = [
    "pop_0_4","pop_5_9","pop_10_14","pop_15_19",
    "pop_20_24","pop_25_29","pop_30_34","pop_35_39","pop_40_44",
    "pop_45_49","pop_50_54","pop_55_59","pop_60_64","pop_65_69",
    "pop_70_74","pop_75_79","pop_80_84","pop_85_89","pop_90_94",
    "pop_95_99","pop_100"]

logger = appbase.AppBase().get_logger()

class Kokusei2015PopulationH03Service(
        service.kokusei2015_population_h.Kokusei2015PopulationHService):

    def __init__(self):
        pass

    def download_save_data_src(self,pref_url):
        logger.info(pref_url)
        
        pref_html = self.get_http_requests( pref_url )
        download_url = self.get_download_url(pref_html,data_name)
        if not download_url:
            logger.warning("fail found download url for "+pref_url)
            return
            
        csv_content = self.get_http_requests( download_url )
        ret_datas = self.load_csv_content( csv_content )
        
        util_db = Db()
        util_db.bulk_upsert("kokusei2015_population_h03",
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

            for col_no in range(12,33):
                if cols[col_no] in ["-","X"]:
                    cols[col_no] = 0
                else:
                    cols[col_no] = int( cols[col_no] )

                col_name = other_cols[col_no-13]
                ret_datas_tmp[pref_city_town][col_name] += cols[col_no]
            
        return self.conv_hash_to_list(ret_datas_tmp)
    

