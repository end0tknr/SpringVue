#!python
# -*- coding: utf-8 -*-

# refer urls are below.
# https://www.land.mlit.go.jp/webland/download.html

from bs4 import BeautifulSoup
from psycopg2  import extras # for bulk insert
from io import BytesIO

import appbase
import copy
import csv
import glob
import json
import xlrd # for xls
import os
import re
import tempfile
import urllib.request
import zipfile
from service.city       import CityService

target_host  = 'https://www.land.mlit.go.jp'
target_path  = '/webland/zip/All_20212_20213.zip'

logger = appbase.AppBase.get_logger()

class MlitFudousanTorihikiService(appbase.AppBase):

    def __init__(self):
        pass

    def save_tbl_rows(self, rows):
        pass

    def __divide_rows(self, org_rows, chunk_size):
        pass
    
    def download_master(self):
        download_url = target_host + target_path
        logger.info(download_url)
        
        ret_data = []
    
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_zip_path =os.path.join(tmp_dir, "tmp.zip")

            try:
                data = urllib.request.urlopen(download_url).read()
                with open(tmp_zip_path, mode="wb") as fh:
                    fh.write(data)

                zip = zipfile.ZipFile(tmp_zip_path, "r")
                zip.extractall(path=tmp_dir)
                zip.close()

            except Exception as e:
                logger.error("fail", download_url)
                logger.error(e)
                return []

            for csv_path in glob.glob(tmp_dir + '/*.csv' ):
                csv_name = str( os.path.split(csv_path)[1] )

                with open(csv_path, encoding='cp932', newline="") as f:
                    read_dict = csv.DictReader(f, delimiter=",", quotechar='"')
                    ks = read_dict.fieldnames
                    return_dict = {k: [] for k in ks}

                    for row in read_dict:
                        for k, v in row.items():
                            return_dict[k].append(v)
                    ret_data.append([csv_name, return_dict])
        return ret_data
        
