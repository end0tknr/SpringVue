#!python
# -*- coding: utf-8 -*-

#refer to
#  https://www.e-stat.go.jp/stat-search/files
#    ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
#      &tclass1=000001129435&tclass2=000001129436

# 持ち家の購入･新築･建て替え等の状況 101-3
#   住宅の建築の時期(7区分)，住宅の購入・新築・建て替え等(8区分)別持ち家数
#   －全国，都道府県，市区町村

from service.city import CityService
from util.db import Db
import re
import service.estat_jutakutochi

download_url = \
    "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031865859&fileKind=0"
insert_cols = ["pref","city",
               "build_year",
               "buy_new",
               "buy_used",
               "build_new",
               "rebuild",
               "inheritance",
               "other"
               ]
insert_sql  = "INSERT INTO estat_jutakutochi_e101 (%s) VALUES %s"
logger = None

class EstatJutakuTochiE101Service(
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

    def del_tbl_rows(self):
        logger.info("start")
        util_db = Db()
        util_db.del_tbl_rows("estat_jutakutochi_e101")

    def save_tbl_rows(self, rows):
        logger.info("start")
        util_db = Db()
        util_db.save_tbl_rows("estat_jutakutochi_e101",insert_cols,rows )

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

            # 住宅の建築の時期
            if row_vals[ 7] =="00_総数":
                continue

            # 例 02_1971～1980年 -> 1971～1980年
            build_year = re_compile.sub("",row_vals[7])

            for col_no in [9,12,15,16,17,18]:
                if row_vals[col_no] == "-":
                    row_vals[col_no] = 0

            new_info = {
                "pref"          :city_def["pref"],
                "city"          :city_def["city"],
                "build_year"    :build_year,
                "buy_new"       :row_vals[9],
                "buy_used"      :row_vals[12],
                "build_new"     :row_vals[15],
                "rebuild"       :row_vals[16],
                "inheritance"   :row_vals[17],
                "other"         :row_vals[18],
            }

            ret_data.append(new_info)
            row_no += 1
            
        return ret_data


    def get_shinchiku_vals_group_by_city(self):
        sql = """
select *
from  estat_jutakutochi_e101
where build_year='2016～2018年9月'
"""
        ret_data = []
        
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:
                try:
                    db_cur.execute(sql)
                except Exception as e:
                    logger.error(e)
                    logger.error(sql)
                    return []
                
                for ret_row in  db_cur.fetchall():
                    ret_data.append( dict( ret_row ))
                
        return ret_data
    
