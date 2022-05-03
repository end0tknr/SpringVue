#!python
# -*- coding: utf-8 -*-

#refer to
#  https://www.e-stat.go.jp/stat-search/files
#    ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
#      &tclass1=000001129435&tclass2=000001129436

# 住宅の設備 30-2
#   住宅の種類(2区分)，住宅の所有の関係(2区分)，建て方(4区分)，構造(2区分)，
#   省エネルギー設備等(7区分)別住宅数－全国，都道府県，市区町村

from service.city import CityService
import re
import service.estat_jutakutochi

download_url = \
    "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031865693&fileKind=0"
insert_cols = ["pref","city",
               "own_type",
               "total",
               "solar_water_heater",
               "pv",
               "double_sash"
               ]
insert_sql  = "INSERT INTO estat_jutakutochi_e030 (%s) VALUES %s"
logger = None

class EstatJutakuTochiE030Service(
        service.estat_jutakutochi.EstatJutakuTochiService):

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
        
        city_service = CityService()
        ret_data = []
        re_compile = re.compile("^\d+_")
        row_no = 0
        
        for row_vals in wsheet.iter_rows(min_row=12, values_only=True):
            row_vals = list(row_vals)
            
            city_code_name_str = row_vals[5]
            city_code_name = city_code_name_str.split("_")
            city_code_name[1] = city_code_name[1].replace("\s","")
            city_code_name[1] = city_code_name[1].replace("　","")

            if row_no % 100 == 0:
                logger.info( "%d %s" % (row_no,city_code_name[1]))

            # 種類 x 建て方 x 構造
            if row_vals[ 7] !="0_総数" or \
               row_vals[11] !="0_総数" or \
               row_vals[13] !="0_総数":
                row_no += 1
                continue

            own_type = row_vals[9]
            if own_type =="0_総数": #住宅の所有
                row_no += 1
                continue

            city_def = city_service.find_def_by_code_city(city_code_name[0],
                                                          city_code_name[1])
            if not city_def or not city_def["city"]:
                row_no += 1
                continue
            
            own_type = re_compile.sub("",own_type)  # 例. 1_持ち家 -> 持ち家

            for col_no in [14,15,17,19,20]:
                if row_vals[col_no] == "-":
                    row_vals[col_no] = 0

            new_info = {
                "pref"         : city_def["pref"],
                "city"         : city_def["city"],
                "own_type"     : own_type,
                "total"             : row_vals[14],
                "solar_water_heater": row_vals[15],
                "pv"                : row_vals[17],
                "double_sash"       :
                int(row_vals[19]) + int(row_vals[20])
            }

            for atri_key in new_info:
                if new_info[atri_key] == "-":
                    new_info[atri_key] = None

            ret_data.append(new_info)
            row_no += 1
            
        return ret_data
