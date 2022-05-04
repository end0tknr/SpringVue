#!python
# -*- coding: utf-8 -*-

#refer to
#  https://www.e-stat.go.jp/stat-search/files
#    ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
#      &tclass1=000001129435&tclass2=000001129436

# 持ち家の増改築・改修工事,高齢者等のための設備工事,
# 耐震改修工事,耐震診断の有無,リフォーム工事の状況 158-4
#   世帯の年間収入階級(5区分)，2014年以降の住宅の増改築・改修工事等(8区分)
#   別持ち家数－全国，都道府県，市区町村

from service.city import CityService
import re
import service.estat_jutakutochi

download_url = \
    "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031904621&fileKind=0"
insert_cols = ["pref","city",
               "year_income",
               "reform_plan",
               "reform_kitchen_bath",
               "reform_floor_inner_wall",
               "reform_roof_outer_wall",
               "reform_pillar_basic",
               "reform_insulation",
               "reform_other"
               ]
insert_sql  = "INSERT INTO estat_jutakutochi_g158 (%s) VALUES %s"
logger = None

class EstatJutakuTochiG158Service(
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

            city_def = city_service.find_def_by_code_city(city_code_name[0],
                                                          city_code_name[1])
            if not city_def or not city_def["city"]:
                row_no += 1
                continue
            
            if row_no % 100 == 0:
                logger.info( "%d %s" % (row_no,city_code_name[1]))

            # 世帯の年間収入階級
            if row_vals[ 7] =="00_総数":
                continue

            # 例 05_300～500万円未満 -> 300～500万円未満
            year_income = re_compile.sub("",row_vals[7])

            for col_no in [10,11,12,13,14,15,16]:
                if row_vals[col_no] == "-":
                    row_vals[col_no] = 0

            new_info = {
                "pref"          :city_def["pref"],
                "city"          :city_def["city"],
                "year_income"   :year_income,
                "reform_plan"            :row_vals[10],
                "reform_kitchen_bath"    :row_vals[11],
                "reform_floor_inner_wall":row_vals[12],
                "reform_roof_outer_wall" :row_vals[13],
                "reform_pillar_basic"    :row_vals[14],
                "reform_insulation"      :row_vals[15],
                "reform_other"           :row_vals[16],
            }

            ret_data.append(new_info)
            row_no += 1
            
        return ret_data
