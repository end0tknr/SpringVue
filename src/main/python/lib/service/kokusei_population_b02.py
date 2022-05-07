#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files
#  ?layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466
# 総人口・総世帯数・男女・年齢・配偶関係 2-7
# 男女，年齢（5歳階級及び3区分），国籍総数か日本人別人口，平均年齢，
# 年齢中位数及び人口構成比［年齢別］－全国，都道府県，
# 市区町村（2000年（平成12年）市区町村含む）

from service.city import CityService
import re
import service.kokusei_population

download_url = \
    "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032142410&fileKind=0"
insert_cols = ["pref","city","pop_0_4","pop_5_9","pop_10_14","pop_15_19",
               "pop_20_24","pop_25_29","pop_30_34","pop_35_39","pop_40_44",
               "pop_45_49","pop_50_54","pop_55_59","pop_60_64","pop_65_69",
               "pop_70_74","pop_75_79","pop_80_84","pop_85_89","pop_90_94",
               "pop_95_99","pop_100"]
insert_sql  = "INSERT INTO kokusei_population_b02 (%s) VALUES %s"
logger = None

class KokuseiPopulationB02Service(
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

            if row_vals[0] != "0_国籍総数" or row_vals[1] != "0_総数":
                continue
            
            city_code = row_vals[7]
            re_result = re_compile.search(row_vals[8])
            if not re_result:
                continue
            city_name = re_result.group(2)
            # print(city_code,city_name)

            city_def = city_service.find_def_by_code_city(city_code,
                                                          city_name)
            if not city_def:
                continue

            for col_no in range(10,31):
                if row_vals[col_no] == "-":
                    row_vals[col_no] = 0
                    
            new_info = {
                "pref"          : city_def["pref"],
                "city"          : city_def["city"],
                "pop_0_4"       :row_vals[10],
                "pop_5_9"       :row_vals[11],
                "pop_10_14"     :row_vals[12],
                "pop_15_19"     :row_vals[13],
                "pop_20_24"     :row_vals[14],
                "pop_25_29"     :row_vals[15],
                "pop_30_34"     :row_vals[16],
                "pop_35_39"     :row_vals[17],
                "pop_40_44"     :row_vals[18],
                "pop_45_49"     :row_vals[19],
                "pop_50_54"     :row_vals[20],
                "pop_55_59"     :row_vals[21],
                "pop_60_64"     :row_vals[22],
                "pop_65_69"     :row_vals[23],
                "pop_70_74"     :row_vals[24],
                "pop_75_79"     :row_vals[25],
                "pop_80_84"     :row_vals[26],
                "pop_85_89"     :row_vals[27],
                "pop_90_94"     :row_vals[28],
                "pop_95_99"     :row_vals[29],
                "pop_100"       :row_vals[30]
            }
            ret_data.append(new_info)

        return ret_data

