#!python
# -*- coding: utf-8 -*-

from util.db import Db

import appbase
from service.city import CityService
import xlrd # for xls , openpyxl for xlsx
import os
import re
import tempfile
import urllib.request

# refer urls are below.
#   https://www.mlit.go.jp/toshi/city_plan/toshi_city_plan_fr_000022.html
download_url = 'https://www.mlit.go.jp/common/000167918.xls'
insert_cols = ["pref","city","area_ha","area_count"]

logger = None

class MlitSeisanRyokuchiService(appbase.AppBase):

    def __init__(self):
        global logger
        logger = self.get_logger()

    def del_tbl_rows(self):
        logger.info("start")
        util_db = Db()
        util_db.del_tbl_rows("mlit_seisanryokuchi")

    def save_tbl_rows(self, rows):
        logger.info("start")
        util_db = Db()
        util_db.save_tbl_rows("mlit_seisanryokuchi",insert_cols,rows )
        

    def download_master(self):
        logger.info(download_url)
        ret_data = []

        with tempfile.TemporaryDirectory() as tmp_dir:
            
            try:
                res = urllib.request.urlopen(download_url)
                
                filename = os.path.basename( download_url )
                tmp_file_path =os.path.join(tmp_dir, filename)
                # print( res.getheaders() )
                
                data = res.read()
                with open(tmp_file_path, mode="wb") as fh:
                    fh.write(data)

                wbook = xlrd.open_workbook(tmp_file_path)
                for sheetname in wbook.sheet_names():
                    wsheet = wbook.sheet_by_name(sheetname)
                    logger.info("start %s %d rows" % (sheetname, wsheet.nrows) )

                    tmp_ret_data = self.__load_wsheet( wsheet )
                    ret_data.extend( tmp_ret_data )

            except Exception as e:
                logger.error("fail", download_url)
                logger.error(e)
                return []

            return ret_data
            
    def __load_wsheet( self, wsheet ):

        city_service = CityService()
        ret_data = []
        ret_data_tmp = {}
        row_no = 19
        re_compile_pref = re.compile("^(.+[都道府県])$")
        pref = ""

        while row_no < wsheet.nrows :

            tmp_pref = wsheet.cell_value(row_no,2)
            tmp_city = wsheet.cell_value(row_no,3)
            re_result = re_compile_pref.search(tmp_pref)
            if re_result and tmp_city == "計":
                pref = re_result.group(1)
                row_no += 1
                continue

            city_def = city_service.find_def_by_pref_city(pref, tmp_city)
            if not city_def or not city_def["city"]:
                row_no += 1
                continue
            

            pref_city = "%s\t%s" %(pref,tmp_city)
            if not pref_city in ret_data_tmp:
                ret_data_tmp[pref_city] = {"area_ha":0,"area_count":0}

            ret_data_tmp[pref_city]["area_ha"]    += wsheet.cell_value(row_no,5)
            ret_data_tmp[pref_city]["area_count"] += wsheet.cell_value(row_no,6)

            row_no += 1
            
        ret_data = []
        for pref_city_str,vals_tmp in ret_data_tmp.items():
            pref_city = pref_city_str.split("\t")
            vals_tmp["pref"] = pref_city[0]
            vals_tmp["city"] = pref_city[1]
            
            ret_data.append(vals_tmp)
        print(ret_data)
        return ret_data


    def get_vals(self):
        sql = """
select *
from mlit_seisanryokuchi
"""
        ret_datas = []
        
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:
                try:
                    db_cur.execute(sql)
                    
                except Exception as e:
                    logger.error(e)
                    logger.error(sql)
                    return []

                city_service = CityService()
                for ret_row in  db_cur.fetchall():
                    ret_row = dict( ret_row )

                    wards = city_service.get_seirei_wards(ret_row["city"])
                    if len(wards) == 0:
                        ret_datas.append(ret_row)
                        continue
                    
                    for ward in wards:
                        ret_row_cp = ret_row.copy()
                        ret_row_cp["city"] = ward["city"]
                        ret_datas.append(ret_row_cp)

        return ret_datas
    
    
