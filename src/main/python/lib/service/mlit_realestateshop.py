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

cgi_base = "https://etsuran.mlit.go.jp/TAKKEN/takkenKensaku.do"

logger = None

class MlitRealEstateShopService(appbase.AppBase):

    def __init__(self):
        global logger
        logger = self.get_logger()

    def del_tbl_rows(self):
        logger.info("start")
        util_db = Db()
        util_db.del_tbl_rows("real_estate_shop")

    def save_tbl_rows(self, rows):
        logger.info("start")
        util_db = Db()
        util_db.save_tbl_rows("real_estate_shop",insert_cols,rows )
        

    def download_master(self):
        logger.info()

