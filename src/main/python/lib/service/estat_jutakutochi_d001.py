#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files
#   ?layout=datalist&toukei=00200522&tstat=000001127155&tclass1=000001133386
# 市区町村-1
#   居住世帯の有無(8区分)別住宅数及び住宅以外で人が
#   居住する建物数―全国，都道府県，市区町村

from service.city import CityService
import service.estat_jutakutochi

download_url = \
    "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031866048&fileKind=0"
insert_cols = ["pref","city","house","lived_house","nolived_house"]
insert_sql  = "INSERT INTO estat_jutakutochi_d001 (%s) VALUES %s"
logger = None

class EstatJutakuTochiD001Service(
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
            if not city_def:
                row_no += 1
                continue
            new_info = {
                "pref"         : city_def["pref"],
                "city"         : city_def["city"],
                "house"        : wsheet.cell_value(row_no,10), # 住宅数
                "lived_house"  : wsheet.cell_value(row_no,11), # 居住世帯あり
                "nolived_house": wsheet.cell_value(row_no,14), # 居住世帯なし
            }

            ret_data.append(new_info)
            
            row_no += 1
        return ret_data

