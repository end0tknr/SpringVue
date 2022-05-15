#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files?toukei=00200521&tstat=000001080615
# 住居の状態 18-2
# 住居の種類・住宅の所有の関係(6区分)別一般世帯数，一般世帯人員及び1世帯当たり人員
# － 都道府県※，都道府県市部・郡部，市区町村※，平成12年市町村

from service.city import CityService
from util.db import Db

import csv
import io
import re
import service.kokusei2015_population

data_src_tbl_no = "18-2"
insert_cols = ["pref","city",
               "owned_house","public_rented","private_rented","company_house"]
insert_sql  = "INSERT INTO kokusei2015_population_018 (%s) VALUES %s"
logger = None

class Kokusei2015Population018Service(
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

    def del_tbl_rows(self):
        logger.info("start")
        util_db = Db()
        util_db.del_tbl_rows("kokusei2015_population_018")

    def save_tbl_rows(self, rows):
        logger.info("start")
        util_db = Db()
        util_db.save_tbl_rows("kokusei2015_population_018",insert_cols,rows )

    def load_csv_content( self, csv_content ):
        
        city_service = CityService()

        f = io.StringIO()
        f.write( csv_content.decode(encoding='cp932') )
        f.seek(0)

        ret_data = []
        for cols in csv.reader( f ):

            city_code = cols[2]
            city_name = cols[6].replace(" ","")
            city_def = city_service.find_def_by_code_city(city_code,city_name)
            if not city_def or not city_def["city"]:
                continue

            # 政令指定都市は、区のレベルで登録
            if city_service.is_seirei_city(city_def["city"]):
                continue

            for col_no in [10,11,12,13]:
                if cols[col_no] == "-":
                    cols[col_no] = 0
                    
            new_info = {
                "pref"          : city_def["pref"],
                "city"          : city_def["city"],
                "owned_house"   : cols[10],
                "public_rented" : cols[11],
                "private_rented": cols[12],
                "company_house" : cols[13]
            }
            ret_data.append(new_info)

        return ret_data
    
