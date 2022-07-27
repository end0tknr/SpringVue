#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files
#  ?layout=datalist&toukei=00200521&tstat=000001136464&cycle=0&tclass1=000001136466
# 総人口・総世帯数・男女・年齢・配偶関係 2-7
# 男女，年齢（5歳階級及び3区分），国籍総数か日本人別人口，平均年齢，
# 年齢中位数及び人口構成比［年齢別］－全国，都道府県，
# 市区町村（2000年（平成12年）市区町村含む）

from service.city                       import CityService
from service.kokusei2015_population_003 import Kokusei2015Population003Service
from util.db      import Db
import re
import service.kokusei_population_b

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

            # 政令指定都市は、区のレベルで登録
            if city_service.is_seirei_city(city_def["city"]):
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

    def del_tbl_rows(self):
        logger.info("start")
        util_db = Db()
        util_db.del_tbl_rows("kokusei_population_b02")

    def save_tbl_rows(self, rows):
        logger.info("start")
        util_db = Db()
        util_db.save_tbl_rows("kokusei_population_b02",insert_cols,rows )
        

    def get_vals(self):
        sql = "select * from kokusei_population_b02"
        
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


    def get_trend(self):
        kokusei2015_pop_003_service = Kokusei2015Population003Service()
        pre_vals_tmp = kokusei2015_pop_003_service.get_vals()

        pre_vals = {}
        for pre_val in pre_vals_tmp:
            pref_city = "\t".join([pre_val["pref"],
                                   pre_val["city"] ])
            del pre_val["pref"]
            del pre_val["city"]
            pre_vals[pref_city] = pre_val

        now_vals = self.get_vals()

        val_keys = ["pop_0_4","pop_5_9","pop_10_14","pop_15_19","pop_20_24",
                    "pop_25_29","pop_30_34","pop_35_39","pop_40_44","pop_45_49",
                    "pop_50_54","pop_55_59","pop_60_64","pop_65_69","pop_70_74",
                    "pop_75_79","pop_80_84","pop_85_89","pop_90_94","pop_95_99",
                    "pop_100"]

        for now_val in now_vals:
            pref_city = "\t".join([now_val["pref"],
                                   now_val["city"] ])
            if not pref_city in pre_vals:
                for val_key in val_keys:
                    now_val[val_key + "_2015"]   = 0
                continue

            for val_key in val_keys:
                now_val[val_key + "_2015"] = pre_vals[pref_city][val_key]
            
        return now_vals

    
    
