#!python
# -*- coding: utf-8 -*-

from psycopg2  import extras # for bulk insert

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
logger = None

class MlitSeisanRyokuchiService(appbase.AppBase):

    def __init__(self):
        global logger
        logger = self.get_logger()

    def save_tbl_rows(self, rows):
        pass
    
    def divide_rows(self, org_rows, chunk_size):
        pass

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
        row_no = 19
        pref = ""

        while row_no < wsheet.nrows :
            cities = wsheet.cell_value(row_no,3)

            tmp_pref = wsheet.cell_value(row_no,2)
            new_info = {
                "city"      : wsheet.cell_value(row_no,3),
                "area_ha"   : wsheet.cell_value(row_no,5),
                "area_count": wsheet.cell_value(row_no,6)
            }

            if not new_info["city"] and \
               not new_info["area_ha"] and \
               not new_info["area_count"]:
                row_no += 1
                continue
                
            if new_info["city"] == "計":
                pref = tmp_pref
                row_no += 1
                continue
            
            city_def = city_service.find_def_by_pref_city(pref, new_info["city"])
            if not city_def:
                row_no += 1
                continue
            
            new_info["city"] = city_def["city"]
            
            ret_data.append(new_info)
            row_no += 1

        return ret_data

    def save_tbl_rows(self, rows):
        logger.info("start")
        logger.info(rows[0])

        bulk_insert_size = self.get_conf()["common"]["bulk_insert_size"]
        atri_keys = ["city","area_ha","area_count"]
        row_groups = self.__divide_rows(rows, bulk_insert_size, atri_keys )
        
        sql = """
INSERT INTO mlit_seisanryokuchi (%s) VALUES %s
  ON CONFLICT DO NOTHING
"""
        sql = sql % (",".join(atri_keys), "%s")
        print(sql)
        print(row_groups)
        
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:

                for row_group in row_groups:
                    try:
                        # bulk insert
                        extras.execute_values(db_cur,sql,row_group)
                    except Exception as e:
                        logger.error(e)
                        logger.error(sql)
                        logger.error(row_group)
                        return False
                    
            db_conn.commit()
        return True

    def __divide_rows(self, org_rows, chunk_size, atri_keys):
        i = 0
        chunk = []
        ret_rows = []
        for org_row in org_rows:
            new_tuple = ()
            for atri_key in atri_keys:
                new_tuple += (org_row[atri_key],)
            chunk.append( new_tuple )
            
            if len(chunk) >= chunk_size:
                ret_rows.append(chunk)
                chunk = []
            i += 1

        if len(chunk) > 0:
            ret_rows.append(chunk)

        return ret_rows
