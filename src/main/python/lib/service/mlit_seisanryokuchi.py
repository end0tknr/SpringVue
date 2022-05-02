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

logger = appbase.AppBase.get_logger()

class MlitSeisanRyokuchiService(appbase.AppBase):

    def __init__(self):
        pass

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
        row_no = 21

        while row_no < wsheet.nrows :
            new_info = {
                "city"      : wsheet.cell_value(row_no,3),
                "area_ha"   : wsheet.cell_value(row_no,5),
                "area_count": wsheet.cell_value(row_no,6)
            }

            if not city_service.find_def_by_city(new_info["city"]):
                row_no += 1
                continue
            
            ret_data.append(new_info)
            row_no += 1

        return ret_data
