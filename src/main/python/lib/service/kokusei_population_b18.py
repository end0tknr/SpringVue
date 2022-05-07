#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files
#  ?layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466
# 住宅の所有関係・住宅の建て方 18-4
# 住宅の所有の関係別一般世帯数－全国，都道府県，
# 市区町村（2000年（平成12年）市区町村含む）

from service.city import CityService
import re
import service.kokusei_population

download_url = \
    "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032142543&fileKind=0"
insert_cols = ["pref","city",
               "owned_house","public_rented","private_rented","company_house"]
insert_sql  = "INSERT INTO kokusei_population_b18 (%s) VALUES %s"
logger = None

class KokuseiPopulationB18Service(
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

