#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files
#  ?layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466
# 世帯の種類・世帯人員・世帯の家族類型 12-3
# 世帯主の男女，世帯主の年齢（5歳階級），世帯の家族類型別一般世帯数
# －全国，都道府県，市区町村
from service.city import CityService
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

            re_result = re_compile.search(row_vals[4])
            if not re_result:
                continue
            owner_age = re_result.group(2)

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

