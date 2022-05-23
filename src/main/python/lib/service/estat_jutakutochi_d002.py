#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files
#   ?layout=datalist&toukei=00200522&tstat=000001127155&tclass1=000001133386
# 市区町村-2
#   住宅の建て方(3区分)，階数(4区分)・構造(2区分)・所有の関係(2区分)・
#   建築の時期(2区分)別住宅数及び世帯の種類(2区分)別世帯数―
#   全国，都道府県，市区町村

from service.city import CityService
import service.estat_jutakutochi

download_url = \
    "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031866049&fileKind=0"
insert_cols = ["pref","city",
               "total",                 #総数
               "detached_house",        #一戸建
               "tenement_houses",       #長屋
               "apartment",             #共同住宅
               "owned_house",           #持ち家
               "rented_house",          #借家
               ]       
insert_sql  = "INSERT INTO estat_jutakutochi_d002 (%s) VALUES %s"
logger = None

class EstatJutakuTochiD002Service(
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
        row_no = 17
        
        while row_no < wsheet.nrows :
            city_code = wsheet.cell_value(row_no,7)
            city_name = wsheet.cell_value(row_no,8).strip()
            # print(city_code, city, total)

            city_def = city_service.find_def_by_code_city(city_code,
                                                          city_name)
            if not city_def or not city_def["city"]:
                row_no += 1
                continue
            new_info = {
                "pref"         : city_def["pref"],
                "city"         : city_def["city"],
                "total"          : wsheet.cell_value(row_no,10),
                "detached_house" : wsheet.cell_value(row_no,11),
                "tenement_houses": wsheet.cell_value(row_no,12),
                "apartment"      : wsheet.cell_value(row_no,13),
                "owned_house"    : wsheet.cell_value(row_no,20),
                "rented_house"   : wsheet.cell_value(row_no,21),
            }
            for atri_key in new_info:
                if new_info[atri_key] == "-":
                    new_info[atri_key] = None

            ret_data.append(new_info)
            
            row_no += 1
        return ret_data

    def get_vals(self):
        sql = "select * from estat_jutakutochi_d002"
        
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
        
