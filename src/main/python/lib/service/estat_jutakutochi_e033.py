#!python
# -*- coding: utf-8 -*-

#refer to
#  https://www.e-stat.go.jp/stat-search/files
#    ?layout=datalist&toukei=00200522&tstat=000001127155&cycle=0
#      &tclass1=000001129435&tclass2=000001129436

# 住宅の設備 33-2
#   住宅の所有の関係(6区分)，腐朽・破損の有無(2区分)，建築の時期(9区分)別住宅数
#    －全国，都道府県，市区町村

from service.city import CityService
import re
import service.estat_jutakutochi

download_url = \
    "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031865698&fileKind=0"
insert_cols = ["pref","city",
               "damage",
               "build_year",
               "owned_house",           #持ち家
               "rented_house",          #借家
               ]
insert_sql  = "INSERT INTO estat_jutakutochi_e033 (%s) VALUES %s"

logger = None

class EstatJutakuTochiE033Service(
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

            # 腐朽・破損の有無 x 住宅の建築の時期
            damage     = row_vals[7]
            build_year = row_vals[9]
            if damage =="0_総数" or build_year =="00_総数":
                row_no += 1
                continue

            # 例 1_腐朽・破損あり -> 腐朽・破損あり
            damage     = re_compile.sub("",damage)
            build_year = re_compile.sub("",build_year)

            
            for col_no in [11,12]:
                if row_vals[col_no] == "-":
                    row_vals[col_no] = 0

            new_info = {
                "pref"         : city_def["pref"],
                "city"         : city_def["city"],
                "damage"       : damage,
                "build_year"   : build_year,
                "owned_house"  : row_vals[11],
                "rented_house" : row_vals[12]
            }

            for atri_key in new_info:
                if new_info[atri_key] == "-":
                    new_info[atri_key] = None

            ret_data.append(new_info)
            row_no += 1
            
        return ret_data


    def parse_build_year_str(self,year_str):

        if year_str == "1970年以前":
            return "0\t1970"
        if year_str == "1971～1980年":
            return "1971\t1980"
        if year_str == "1981～1990年":
            return "1981\t1990"
        if year_str in ["1991～1995年","1996～2000年"]:
            return "1991\t2000"
        if year_str in ["2001～2005年","2006～2010年"]:
            return "2001\t2010"
        if year_str == "2011～2015年":
            return "2011\t2015"
        if year_str == "2016～2018年9月":
            return "2016\t2018"
        
        return None
    

    def get_group_by_city(self):
        sql = "select * from estat_jutakutochi_e033"
        
        ret_data_tmp = {}
        
        db_conn = self.db_connect()
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute(sql)
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return []
            
            for ret_row in  db_cur.fetchall():
                ret_row = dict( ret_row )

                if not ret_row["city"]:
                    continue
                
                pref_city = "%s\t%s" % ( ret_row["pref"],ret_row["city"])
                if not pref_city in ret_data_tmp:
                    ret_data_tmp[pref_city] = {}

                build_year = self.parse_build_year_str( ret_row["build_year"] )

                if not build_year in ret_data_tmp[pref_city]:
                    ret_data_tmp[pref_city][build_year] = {}

                has_damage  = ret_row["damage"]
                owned_house = ret_row["owned_house"]
                if not has_damage in ret_data_tmp[pref_city][build_year]:
                    ret_data_tmp[pref_city][build_year][has_damage] = 0

                ret_data_tmp[pref_city][build_year][has_damage] += owned_house

        ret_datas = []
        for pref_city, ret_data in ret_data_tmp.items():
            (ret_data["pref"],ret_data["city"]) = pref_city.split("\t")
            ret_datas.append(ret_data)
            
        return ret_datas
        
