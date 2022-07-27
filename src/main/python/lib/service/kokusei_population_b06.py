#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files
#  ?layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466
# 世帯の種類・世帯人員・世帯の家族類型 6-3
# 世帯人員の人数別一般世帯数，会社などの独身寮の単身者数，
# 間借り・下宿などの単身者数，一般世帯人員及び一般世帯の1世帯当たり人員－全国，
# 都道府県，市区町村
from service.city import CityService
import re
import service.kokusei_population_b

download_url = \
    "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032142483&fileKind=0"
insert_cols = ["pref","city","setai_total","setai_1","setai_pop"]
insert_sql  = "INSERT INTO kokusei_population_b06 (%s) VALUES %s"
logger = None

class KokuseiPopulationB06Service(
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
        
        re_compile = re.compile("(\d+)_(.+)")
        city_service = CityService()
        ret_data = []
        
        for row_vals in wsheet.iter_rows(min_row=15, values_only=True):
            row_vals = list(row_vals)

            re_result = re_compile.search(row_vals[2])
            if not re_result:
                continue
            city_code = re_result.group(1)
            city_name = re_result.group(2)

            city_def = city_service.find_def_by_code_city(city_code,
                                                          city_name)
            if not city_def:
                continue

            for col_no in [3,4,15]:
                if row_vals[col_no] == "-":
                    row_vals[col_no] = 0
                    
            new_info = {
                "pref"          : city_def["pref"],
                "city"          : city_def["city"],
                "setai_total"   : row_vals[3],
                "setai_1"       : row_vals[4],
                "setai_pop"     : row_vals[15]
            }
            ret_data.append(new_info)

        return ret_data

