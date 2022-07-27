#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files
#  ?layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466
# 住宅の所有関係・住宅の建て方 18-4
# 住宅の所有の関係別一般世帯数－全国，都道府県，
# 市区町村（2000年（平成12年）市区町村含む）

from service.city import CityService
from service.kokusei2015_population_018 import Kokusei2015Population018Service
from util.db import Db

import re
import service.kokusei_population_b

download_url = \
    "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032142543&fileKind=0"
insert_cols = ["pref","city",
               "owned_house","public_rented","private_rented","company_house"]
insert_sql  = "INSERT INTO kokusei_population_b18 (%s) VALUES %s"
logger = None

class KokuseiPopulationB18Service(
        service.kokusei_population_b.KokuseiPopulationService):

    def __init__(self):
        global logger
        logger = self.get_logger()

    def get_download_url(self):
        return download_url
    
    def get_insert_cols(self):
        return insert_cols
    
    def get_insert_sql(self):
        return insert_sql

    def del_tbl_rows(self):
        logger.info("start")
        util_db = Db()
        util_db.del_tbl_rows("kokusei_population_b18")

    def save_tbl_rows(self, rows):
        logger.info("start")
        util_db = Db()
        util_db.save_tbl_rows("kokusei_population_b18",insert_cols,rows )


    def load_wsheet( self, wsheet ):
        
        re_compile = re.compile("^(\d+)_(.+)")
        city_service = CityService()
        ret_data = []
        
        for row_vals in wsheet.iter_rows(min_row=10, values_only=True):
            row_vals = list(row_vals)

            city_code = row_vals[5]

            re_result = re_compile.search(row_vals[6])
            if not re_result:
                continue
            city_name = re_result.group(2)

            city_def = city_service.find_def_by_code_city(city_code,
                                                          city_name)
            if not city_def:
                continue

            # 政令指定都市は、区のレベルで登録
            if city_service.is_seirei_city(city_def["city"]):
                continue
            
            for col_no in [10,11,12,13]:
                if row_vals[col_no] == "-":
                    row_vals[col_no] = 0
                    
            new_info = {
                "pref"          : city_def["pref"],
                "city"          : city_def["city"],
                "owned_house"   : row_vals[10],
                "public_rented" : row_vals[11],
                "private_rented": row_vals[12],
                "company_house" : row_vals[13]
            }
            ret_data.append(new_info)

        return ret_data


    def get_trend_group_by_city(self):
        kokusei2015_pop_018_service = Kokusei2015Population018Service()
        pre_vals_tmp = kokusei2015_pop_018_service.get_group_by_city()

        pre_vals = {}
        for pre_val in pre_vals_tmp:
            pref_city = "\t".join([pre_val["pref"],pre_val["city"]])

            del pre_val["pref"]
            del pre_val["city"]

            pre_vals[pref_city] = pre_val

        now_vals = self.get_group_by_city()
            
        for now_val in now_vals:
            pref_city = "\t".join([now_val["pref"],now_val["city"]])
            if not pref_city in pre_vals:
                now_val["owned_house_2015"]    = 0
                now_val["public_rented_2015"]  = 0
                now_val["private_rented_2015"] = 0
                now_val["company_house_2015"]  = 0
                continue
        
            now_val["owned_house_2015"]    = pre_vals[pref_city]["owned_house"]
            now_val["public_rented_2015"]  = pre_vals[pref_city]["public_rented"]
            now_val["private_rented_2015"] = pre_vals[pref_city]["private_rented"]
            now_val["company_house_2015"]  = pre_vals[pref_city]["company_house"]

        return now_vals
    
        
    def get_group_by_city(self):
        sql = "select * from kokusei_population_b18"
        
        ret_data = []
        db_conn = self.db_connect():
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute(sql)
                for ret_row in  db_cur.fetchall():
                    ret_data.append( dict( ret_row ))
                    
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return []
        return ret_data
