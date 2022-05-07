#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files?toukei=00200521&tstat=000001080615
# 世帯数・世帯人員 7
# 世帯の種類(2区分)，施設等の世帯の種類(6区分)，世帯人員(10区分/4区分)別世帯数，
# 世帯人員及び1世帯当たり人員(間借り・下宿などの単身者及び会社などの独身寮の
# 単身者－特掲) － 都道府県※，都道府県市部・郡部，市区町村※，平成12年市町村

from service.city import CityService
import csv
import io
import re
import service.kokusei2015_population

data_src_tbl_no = "7"
insert_cols = ["pref","city","setai_total","setai_1","setai_pop"]
insert_sql  = "INSERT INTO kokusei2015_population_007 (%s) VALUES %s"
logger = None

class Kokusei2015Population007Service(
        service.kokusei2015_population.Kokusei2015PopulationService):

    def __init__(self):
        global logger
        logger = self.get_logger()

    def get_data_src_tbl_no(self):
        return data_src_tbl_no
    
    def get_insert_cols(self):
        return insert_cols
    
    def get_insert_sql(self):
        return insert_sql

    def load_csv_content( self, csv_content ):
        
        city_service = CityService()
        ret_data = []

        f = io.StringIO()
        f.write( csv_content.decode(encoding='cp932') )
        f.seek(0)
        for cols in csv.reader( f ):

            city_code = cols[2]
            city_name = cols[6].replace(' ','')
            city_def = city_service.find_def_by_code_city(city_code,city_name)
            if not city_def or not city_def["city"]:
                continue

            for col_no in [9,10,21]:
                if cols[col_no] =="-":
                    cols[col_no] = 0 
        
            new_info = {
                "pref"          :city_def["pref"],
                "city"          :city_def["city"],
                "setai_total"   :cols[9],
                "setai_1"       :cols[10],
                "setai_pop"     :cols[21]
            }
            ret_data.append(new_info)
            
        return ret_data
