#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files?toukei=00200521&tstat=000001080615
# 世帯数・世帯人員 7
# 世帯の種類(2区分)，施設等の世帯の種類(6区分)，世帯人員(10区分/4区分)別世帯数，
# 世帯人員及び1世帯当たり人員(間借り・下宿などの単身者及び会社などの独身寮の単身者
# －特掲) － 都道府県※，都道府県市部・郡部，市区町村※，平成12年市町村

from service.city import CityService
import csv
import io
import re
import service.kokusei2015_population

data_src_tbl_no = "13-2"
insert_cols = ["pref","city","owner_age","total_setai","family_setai",
               "other_setai","single_setai","unknown_setai"]
insert_sql  = "INSERT INTO kokusei2015_population_013 (%s) VALUES %s"
logger = None

class Kokusei2015Population013Service(
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

        f = io.StringIO()
        f.write( csv_content.decode(encoding='cp932') )
        f.seek(0)

        ret_data = []
        city_def = None
        re_compile_1 = re.compile("^(\d+) ([^\d]+)$")
        re_compile_2 = re.compile("^\d+.*歳")

        for cols in csv.reader( f ):
            cols[8] = cols[8].strip() 

            if not city_def:
                re_result = re_compile_1.search(cols[8])
                if not re_result:
                    continue

                city_code = re_result.group(1)
                city_name = re_result.group(2)
                city_def = city_service.find_def_by_code_city(city_code,city_name)
                if not city_def or not city_def["city"]:
                    city_def = None
                continue

            if cols[8] == "総数（男女別）":
                continue
            
            re_result = re_compile_2.search(cols[8])
            if not re_result:
                city_def = None
                continue

            for col_no in [9,10,26,27,28]:
                if cols[col_no] =="-":
                    cols[col_no] = 0
        
            new_info = {
                "pref"          :city_def["pref"],
                "city"          :city_def["city"],
                "owner_age"     :cols[8],
                "total_setai"   :cols[9],
                "family_setai"  :cols[10],
                "other_setai"   :cols[27],
                "single_setai"  :cols[28],
                "unknown_setai" :cols[26],
            }
            ret_data.append(new_info)

        return ret_data
