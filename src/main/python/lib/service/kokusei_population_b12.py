#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files
#  ?layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466
# 世帯の種類・世帯人員・世帯の家族類型 12-3
# 世帯主の男女，世帯主の年齢（5歳階級），世帯の家族類型別一般世帯数
# －全国，都道府県，市区町村
from service.city import CityService
from service.kokusei2015_population_013 import Kokusei2015Population013Service
from util.db import Db

import re
import service.kokusei_population

download_url = \
    "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032142506&fileKind=0"
insert_cols = ["pref","city","owner_age","total_setai","family_setai",
               "other_setai","single_setai","unknown_setai"]
insert_sql  = "INSERT INTO kokusei_population_b12 (%s) VALUES %s"
logger = None

class KokuseiPopulationB12Service(
        service.kokusei_population.KokuseiPopulationService):

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
        util_db.del_tbl_rows("kokusei_population_b12")

    def save_tbl_rows(self, rows):
        logger.info("start")
        util_db = Db()
        util_db.save_tbl_rows("kokusei_population_b12",insert_cols,rows )

    def load_wsheet( self, wsheet ):
        
        re_compile = re.compile("^(\d+)_(.+)")
        city_service = CityService()
        ret_data = []
        
        for row_vals in wsheet.iter_rows(min_row=15, values_only=True):
            row_vals = list(row_vals)

            if row_vals[3]!="0_総数" or row_vals[4]=="00_総数":
                continue

            re_result = re_compile.search(row_vals[2])
            if not re_result:
                continue
            city_code = re_result.group(1)
            city_name = re_result.group(2)

            city_def = city_service.find_def_by_code_city(city_code,
                                                          city_name)
            if not city_def:
                continue

            # 政令指定都市は、区のレベルで登録
            if city_service.is_seirei_city(city_def["city"]):
                continue

            re_result = re_compile.search(row_vals[4])
            if not re_result:
                continue
            owner_age = re_result.group(2)
            if owner_age == "年齢「不詳」":
                continue

            for col_no in [5,6,23,24,25]:
                if row_vals[col_no] == "-":
                    row_vals[col_no] = 0
                    
            new_info = {
                "pref"          : city_def["pref"],
                "city"          : city_def["city"],
                "owner_age"     : owner_age,
                "total_setai"   : row_vals[5],
                "family_setai"  : row_vals[6],
                "other_setai"   : row_vals[23],
                "single_setai"  : row_vals[24],
                "unknown_setai" : row_vals[25]
            }
            ret_data.append(new_info)

        return ret_data

    def get_trend(self):
        kokusei2015_pop_013_service = Kokusei2015Population013Service()
        pre_vals_tmp = kokusei2015_pop_013_service.get_vals()

        pre_vals = {}
        for pre_val in pre_vals_tmp:
            pref_city_age = "\t".join([pre_val["pref"],
                                       pre_val["city"],
                                       pre_val["owner_age"] ])
            del pre_val["pref"]
            del pre_val["city"]
            del pre_val["owner_age"]

            pre_vals[pref_city_age] = pre_val

        now_vals = self.get_vals()
            
        for now_val in now_vals:
            pref_city_age = "\t".join([now_val["pref"],
                                       now_val["city"],
                                       now_val["owner_age"] ])
            if not pref_city_age in pre_vals:
                now_val["total_setai_2015"]   = 0
                now_val["family_setai_2015"]  = 0
                now_val["other_setai_2015"]   = 0
                now_val["single_setai_2015"]  = 0
                now_val["unknown_setai_2015"] = 0
                continue

            now_val["total_setai_2015"]   = pre_vals[pref_city_age]["total_setai"]
            now_val["family_setai_2015"]  = pre_vals[pref_city_age]["family_setai"]
            now_val["other_setai_2015"]   = pre_vals[pref_city_age]["other_setai"]
            now_val["single_setai_2015"]  = pre_vals[pref_city_age]["single_setai"]
            now_val["unknown_setai_2015"] = pre_vals[pref_city_age]["unknown_setai"]
            
        return now_vals

    
    def get_trend_group_by_city(self):
        kokusei2015_pop_013_service = Kokusei2015Population013Service()
        pre_vals_tmp = kokusei2015_pop_013_service.get_group_by_city()

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
                now_val["total_setai_2015"]   = 0
                now_val["family_setai_2015"]  = 0
                now_val["other_setai_2015"]   = 0
                now_val["single_setai_2015"]  = 0
                now_val["unknown_setai_2015"] = 0
                continue

            now_val["total_setai_2015"]   = pre_vals[pref_city]["total_setai"]
            now_val["family_setai_2015"]  = pre_vals[pref_city]["family_setai"]
            now_val["other_setai_2015"]   = pre_vals[pref_city]["other_setai"]
            now_val["single_setai_2015"]  = pre_vals[pref_city]["single_setai"]
            now_val["unknown_setai_2015"] = pre_vals[pref_city]["unknown_setai"]
            
        return now_vals

    
    def get_group_by_city(self):
        sql = """
select
  pref, city,
  sum( total_setai  ) as total_setai,
  sum( family_setai ) as family_setai,
  sum( other_setai  ) as other_setai,
  sum( single_setai ) as single_setai,
  sum( unknown_setai) as unknown_setai
from kokusei_population_b12
group by pref, city
"""
        
        ret_data = []
        
        with self.db_connect() as db_conn:
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
    
    
    def get_vals(self):
        sql = "select * from kokusei_population_b12"
        
        ret_data = []
        
        with self.db_connect() as db_conn:
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
