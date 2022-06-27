#!python
# -*- coding: utf-8 -*-

from service.newbuild import NewBuildService
from util.db import Db
import appbase
import datetime
import re

logger = NewBuildService().get_logger()

class SumStockService(NewBuildService):

    def __init__(self):
        pass

    def build_type(self):
        return "中古戸建"
    
    def tbl_name_header(self):
        return "sumstock"

