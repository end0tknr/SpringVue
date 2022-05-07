#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files?toukei=00200521&tstat=000001080615
# 男女・年齢・配偶関係 3-2
# 年齢(各歳)，男女別人口，年齢別割合，平均年齢及び年齢中位数(総数及び日本人)
# － 都道府県※，都道府県市部・郡部，市区町村※，平成12年市町村

from service.city import CityService
import csv
import io
import re
import service.kokusei2015_population

data_src_tbl_no = "3-2"

insert_cols = ["pref","city","pop_0_4","pop_5_9","pop_10_14","pop_15_19",
               "pop_20_24","pop_25_29","pop_30_34","pop_35_39","pop_40_44",
               "pop_45_49","pop_50_54","pop_55_59","pop_60_64","pop_65_69",
               "pop_70_74","pop_75_79","pop_80_84","pop_85_89","pop_90_94",
               "pop_95_99","pop_100"]
insert_sql  = "INSERT INTO kokusei2015_population_003 (%s) VALUES %s"
logger = None

class Kokusei2015Population003Service(
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

    def load_csv_content( self, csv_content ):
        
        city_service = CityService()
        ret_data = []

        f = io.StringIO()
        f.write( csv_content.decode(encoding='cp932') )
        f.seek(0)
        for cols in csv.reader( f ):

            if cols[1] != "0101": #=総数
                continue

            city_code = cols[2]
            city_name = cols[6].replace(' ','')
            city_def = city_service.find_def_by_code_city(city_code,city_name)
            if not city_def:
                continue

            for col_no in range(112,133):
                if cols[col_no] =="-":
                    cols[col_no] = 0 
        
            new_info = {
                "pref"          :city_def["pref"],
                "city"          :city_def["city"],
                "pop_0_4"       :cols[112],
                "pop_5_9"       :cols[113],
                "pop_10_14"     :cols[114],
                "pop_15_19"     :cols[115],
                "pop_20_24"     :cols[116],
                "pop_25_29"     :cols[117],
                "pop_30_34"     :cols[118],
                "pop_35_39"     :cols[119],
                "pop_40_44"     :cols[120],
                "pop_45_49"     :cols[121],
                "pop_50_54"     :cols[122],
                "pop_55_59"     :cols[123],
                "pop_60_64"     :cols[124],
                "pop_65_69"     :cols[125],
                "pop_70_74"     :cols[126],
                "pop_75_79"     :cols[127],
                "pop_80_84"     :cols[128],
                "pop_85_89"     :cols[129],
                "pop_90_94"     :cols[130],
                "pop_95_99"     :cols[131],
                "pop_100"       :cols[132]
            }
            ret_data.append(new_info)
            
        return ret_data
