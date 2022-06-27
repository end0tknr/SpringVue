#!python
# -*- coding: utf-8 -*-

from service.newbuild import NewBuildService
from util.db import Db
import appbase
import datetime
import re

logger = None

class SumStockService(NewBuildService):

    def __init__(self):
        global logger
        logger = self.get_logger()

    def build_type():
        return "中古戸建"
    
    def tbl_name_header():
        return "stock"

