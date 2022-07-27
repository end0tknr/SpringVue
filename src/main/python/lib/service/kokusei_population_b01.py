#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files
#  ?layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466
# 総人口・総世帯数・男女・年齢・配偶関係 1-1
#   男女別人口，世帯の種類別世帯数及び世帯人員並びに2015年（平成27年）の人口
#   （組替），2015年（平成27年）の世帯数（組替），5年間の人口増減数，
#   5年間の人口増減率，5年間の世帯増減数，5年間の世帯増減率，人口性比，
#   面積（参考）及び人口密度－全国，都道府県，市区町村（2000年（平成12年）
#   市区町村含む）

from service.city import CityService
from util.db import Db

import re
import service.kokusei_population_b

download_url = \
    "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032142402&fileKind=0"
insert_cols = ["pref","city","pop","pop_2015","pop_density","setai","setai_2015"]
insert_sql  = "INSERT INTO kokusei_population_b01 (%s) VALUES %s"
logger = None

class KokuseiPopulationB01Service(
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
        util_db.del_tbl_rows("kokusei_population_b01")

    def save_tbl_rows(self, rows):
        logger.info("start")
        util_db = Db()
        util_db.save_tbl_rows("kokusei_population_b01",insert_cols,rows )

    def load_wsheet( self, wsheet ):
        
        re_compile = re.compile("(\d+)_(.+)")
        city_service = CityService()
        ret_data = []

        pref_cities = {}
        
        for row_vals in wsheet.iter_rows(min_row=15, values_only=True):
            row_vals = list(row_vals)

            city_code = row_vals[5]
            re_result = re_compile.search(row_vals[6])
            if not re_result:
                continue
            city_name = re_result.group(2)
            # print(city_code,city_name)

            city_def = city_service.find_def_by_code_city(city_code,
                                                          city_name)
            if not city_def:
                continue

            # 政令指定都市は、区のレベルで登録
            if city_service.is_seirei_city(city_def["city"]):
                continue

            for col_no in [7,10,15,16,19]:
                if row_vals[col_no] == "-":
                    row_vals[col_no]  = 0
                    
            new_info = {
                "pref"          : city_def["pref"],
                "city"          : city_def["city"],
                "pop"           : row_vals[7],
                "pop_2015"      : row_vals[10],
                "pop_density"   : row_vals[15],
                "setai"         : row_vals[16],
                "setai_2015"    : row_vals[19]
            }

            ret_data.append(new_info)

        return ret_data
    
    def get_group_by_city(self):
        sql = "select * from kokusei_population_b01"
        
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


