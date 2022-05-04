#!python
# -*- coding: utf-8 -*-

#refer to
#  https://www.e-stat.go.jp/stat-search/files
#    ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
#      &tclass1=000001129435&tclass2=000001129436

# 家計を主に支える者と住居 48-2
#   住宅の建築の時期(7区分)，建て方(2区分)，
#   構造(2区分)別家計を主に支える者の年齢(6区分)別主世帯数及び平均年齢
#   －全国，都道府県，市区町村

from service.city import CityService
import re
import service.estat_jutakutochi

download_url = \
    "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031865771&fileKind=0"
insert_cols = ["pref","city",
               "build_year",
               "owner_age_24",
               "owner_age_25_34",
               "owner_age_35_44",
               "owner_age_45_54",
               "owner_age_55_64",
               "owner_age_65",
               "owner_age_unknown"
               ]
insert_sql  = "INSERT INTO estat_jutakutochi_e048 (%s) VALUES %s"
logger = None

class EstatJutakuTochiE048Service(
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

            # 住宅の建築の時期 x 住宅の建て方 x 建物の構造
            if row_vals[ 7] =="00_総数" or \
               row_vals[ 9] !="00_総数" or \
               row_vals[11] != "0_総数":
                row_no += 1
                continue

            # 例 02_1971～1980年 -> 1971～1980年
            build_year  = re_compile.sub("",row_vals[7])

            for col_no in [13,14,15,16,17,18,19]:
                if row_vals[col_no] == "-":
                    row_vals[col_no] = 0

            new_info = {
                "pref"         : city_def["pref"],
                "city"         : city_def["city"],
                "build_year"   : build_year,
                "owner_age_24"   :      row_vals[13],
                "owner_age_25_34":      row_vals[14],
                "owner_age_35_44":      row_vals[15],
                "owner_age_45_54":      row_vals[16],
                "owner_age_55_64":      row_vals[17],
                "owner_age_65"   :       row_vals[18],
                "owner_age_unknown":    row_vals[19]
            }

            

            ret_data.append(new_info)
            row_no += 1
            
        return ret_data
