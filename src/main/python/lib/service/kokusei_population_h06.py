#!python
# -*- coding: utf-8 -*-

#refer to
# https://www.e-stat.go.jp/stat-search/files?page=1&toukei=00200521&tstat=000001136464&tclass1=000001136472
# 6-1 世帯の家族類型，世帯員の年齢による世帯の種類別一般世帯数－町丁・字等

from service.city import CityService
from util.db      import Db
import appbase
import csv
import io
import re
import service.kokusei_population_h

data_name = "世帯の家族類型，世帯員の年齢による世帯の種類別一般世帯数－町丁・字等"
pkey_cols  = ["pref","city","town"]
other_cols = ["total_setai", "family_setai","other_setai",
              "single_setai","unknown_setai" ]

logger = appbase.AppBase().get_logger()

class KokuseiPopulationH06Service(
        service.kokusei_population_h.KokuseiPopulationHService):

    def __init__(self):
        pass

    def get_all_2020_2015(self):
        sql = """
SELECT
  tbl20.*,
  tbl15.total_setai   as total_setai_2015,
  tbl15.family_setai  as family_setai_2015,
  tbl15.other_setai   as other_setai_2015,
  tbl15.single_setai  as single_setai_2015,
  tbl15.unknown_setai as unknown_setai_2015
FROM kokusei_population_h06 tbl20
JOIN kokusei2015_population_h06 tbl15
ON (tbl20.pref=tbl15.pref AND
    tbl20.city=tbl15.city AND
    tbl20.town=tbl15.town )
"""
        ret_data = []
        db_conn = self.db_connect()
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

        
    def download_save_data_src(self,pref_url):

        pref_html = self.get_http_requests( pref_url )
        download_url = self.get_download_url(pref_html,data_name)
        csv_content = self.get_http_requests( download_url )
        ret_datas = self.load_csv_content( csv_content )
        
        util_db = Db()
        util_db.bulk_upsert("kokusei_population_h06",
                            pkey_cols,
                            pkey_cols + other_cols,
                            other_cols,
                            ret_datas )
            
    def load_csv_content( self, csv_content ):
        city_service = CityService()
        ret_datas_tmp = {}

        f = io.StringIO()
        f.write( csv_content.decode(encoding='cp932') )
        f.seek(0)
        for cols in csv.reader( f ):

            if cols[1] != "総数":
                continue

            pref_name = cols[8]
            city_name = cols[9]
            town_name = cols[10]
            if not pref_name or \
               not city_name or \
               not town_name or \
               cols[11]: # 丁番地 lebelは db登録対象外
                continue

            # 「宮ケ丘（番地）」のような()付は db登録対象外
            if "（" in town_name:
                continue

            city_def = city_service.find_def_by_pref_city(pref_name,
                                                          city_name)
            if not city_def:
                continue

            pref_city_town = "\t".join([pref_name,city_name,town_name])

            if not pref_city_town in ret_datas_tmp:
                ret_datas_tmp[pref_city_town] = {}
                for col_name in other_cols:
                    ret_datas_tmp[pref_city_town][col_name] = 0

            i = 0
            for col_no in [12,13,18,19,20]:
                if cols[col_no] in ["-","X"]:
                    cols[col_no] = 0
                else:
                    cols[col_no] = int( cols[col_no] )

                col_name = other_cols[i]
                ret_datas_tmp[pref_city_town][col_name] += cols[col_no]
                i += 1
            
        return self.conv_hash_to_list(ret_datas_tmp)
