#!python
# -*- coding: utf-8 -*-

#refer to
#  https://www.e-stat.go.jp/stat-search/files
#    ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
#      &tclass1=000001129435&tclass2=000001129436

# 家計を主に支える者と住居 49-2
#   家計を主に支える者の年齢(6区分)別世帯の１か月当たり家賃(10区分)
#   別借家に居住する主世帯数及び１か月当たり家賃－全国，都道府県，市区町村

from service.city import CityService
from util.db      import Db
import re
import service.estat_jutakutochi

download_url = \
    "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031865773&fileKind=0"
insert_cols = ["pref","city",
               "owner_age",
               "rent_0",
               "rent_1_9999",
               "rent_10000_19999",
               "rent_20000_39999",
               "rent_40000_59999",
               "rent_60000_79999",
               "rent_80000_99999",
               "rent_100000_149999",
               "rent_150000_199999",
               "rent_200000",
               "rent_unknown"
               ]
insert_sql  = "INSERT INTO estat_jutakutochi_e049 (%s) VALUES %s"
logger = None

class EstatJutakuTochiE049Service(
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
            
            # 政令指定都市は、区のレベルで登録
            if city_service.is_seirei_city(city_def["city"]):
                row_no += 1
                continue

            if row_no % 100 == 0:
                logger.info( "%d %s" % (row_no,city_code_name[1]))

            # 家計を主に支える者の年齢
            if row_vals[ 7] =="00_総数":
                continue

            # 例 02_25～34歳 -> 25～34歳
            owner_age = re_compile.sub("",row_vals[7])

            for col_no in [9,10,11,12,13,14,15,16,17,18,19]:
                if row_vals[col_no] == "-":
                    row_vals[col_no] = 0

            new_info = {
                "pref"         : city_def["pref"],
                "city"         : city_def["city"],
                "owner_age"    : owner_age,
                "rent_0"             :row_vals[ 9],
                "rent_1_9999"        :row_vals[10],
                "rent_10000_19999"   :row_vals[11],
                "rent_20000_39999"   :row_vals[12],
                "rent_40000_59999"   :row_vals[13],
                "rent_60000_79999"   :row_vals[14],
                "rent_80000_99999"   :row_vals[15],
                "rent_100000_149999" :row_vals[16],
                "rent_150000_199999" :row_vals[17],
                "rent_200000"        :row_vals[18],
                "rent_unknown"       :row_vals[19]
            }

            ret_data.append(new_info)
            row_no += 1
            
        return ret_data

    def del_tbl_rows(self):
        logger.info("start")
        util_db = Db()
        util_db.del_tbl_rows("estat_jutakutochi_e049")

    def save_tbl_rows(self, rows):
        logger.info("start")
        util_db = Db()
        util_db.save_tbl_rows("estat_jutakutochi_e049",insert_cols,rows )
    

    def get_vals(self):
        sql = "select * from estat_jutakutochi_e049"
        
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
        
