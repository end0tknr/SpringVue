#!python
# -*- coding: utf-8 -*-

#refer to
#  https://www.e-stat.go.jp/stat-search/files
#    ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
#      &tclass1=000001129435&tclass2=000001129436

# 住宅の設備 44-4
#   世帯の年間収入階級(9区分)，世帯の種類(2区分)，
#   住宅の所有の関係(5区分)別普通世帯数，１世帯当たり人員，
#   １世帯当たり居住室数及び１世帯当たり居住室の畳数－全国，都道府県，市区町村

from service.city import CityService
from util.db      import Db
import re
import service.estat_jutakutochi

download_url = \
    "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031865704&fileKind=0"
insert_cols = ["pref","city",
               "own_type",
               "year_income",
               "setai"
               ]
insert_sql  = "INSERT INTO estat_jutakutochi_e044 (%s) VALUES %s"
logger = None

class EstatJutakuTochiE044Service(
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

            # 世帯の種類 x 住宅の所有の関係 x 世帯の年収
            if row_vals[7] !="1_主世帯" or \
               not row_vals[9] in ["1_持ち家","2_借家"] or \
               row_vals[11] == "00_総数":
                row_no += 1
                continue

            # 例 1_持ち家 -> 持ち家
            own_type    = re_compile.sub("",row_vals[9])
            year_income = re_compile.sub("",row_vals[11])

            if row_vals[12] == "-":
                setai = 0
            else:
                setai = row_vals[12]

            new_info = {
                "pref"         : city_def["pref"],
                "city"         : city_def["city"],
                "own_type"     : own_type,
                "year_income"  : year_income,
                "setai"        : setai
            }

            ret_data.append(new_info)
            row_no += 1
            
        return ret_data


    def get_group_by_city_income(self):
        sql = """
select *
from estat_jutakutochi_e044
order by pref,city,year_income,own_type
"""
        pre_pref_city = None
        ret_data_tmp = {}
        
        db_conn = self.db_connect()
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute(sql)
                for ret_row in  db_cur.fetchall():
                    ret_row = dict( ret_row )
                    pref_city_income = "\t".join([ ret_row["pref"],
                                                   ret_row["city"],
                                                   ret_row["year_income"] ])
                    if not pref_city_income in ret_data_tmp:
                        ret_data_tmp[pref_city_income] = {}

                    own_type = ret_row["own_type"]
                    ret_data_tmp[pref_city_income][own_type] = \
                        ret_row["setai"]

            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return []
                
        ret_data = []
        for pref_city_income in ret_data_tmp:
            keys = pref_city_income.split("\t")
            vals = ret_data_tmp[pref_city_income]
            vals["pref"]        = keys[0]
            vals["city"]        = keys[1]
            vals["year_income"] = keys[2]
            ret_data.append(vals)
            
        return ret_data
    
    def del_tbl_rows(self):
        logger.info("start")
        util_db = Db()
        util_db.del_tbl_rows("estat_jutakutochi_e044")

    def save_tbl_rows(self, rows):
        logger.info("start")
        util_db = Db()
        util_db.save_tbl_rows("estat_jutakutochi_e044",insert_cols,rows )
