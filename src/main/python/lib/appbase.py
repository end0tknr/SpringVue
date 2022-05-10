#!python
# -*- coding: utf-8 -*-

import json
import logging.config
import os
import psycopg2
import psycopg2.extras
import sys

from selenium import webdriver # ex. pip install selenium==4.0.0a7
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

conf_src = \
    os.path.join(os.path.dirname(__file__),
                 '../../resources/app_py_conf.json')
conf = json.load( open(conf_src) )

logging.config.dictConfig( conf["logging"] )
logger = logging.getLogger()
db_conn = None

class AppBase():
    
    def __init__(self):
        pass

    def get_conf(self):
        return conf

    def get_logger(self):
        return logger

    def db_cursor(self,db_conn):
        return db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
    def db_connect(self):
        global db_conn
        
        if db_conn:
            return db_conn
        
        db_conn = psycopg2.connect(
            database    = conf["db"]["db_name"],
            user        = conf["db"]["db_user"],
            password    = conf["db"]["db_pass"],
            host        = conf["db"]["db_host"],
            port        = conf["db"]["db_port"] )
        return db_conn

    def get_browser(self):
        selenium_conf = conf["selenium"]
        browser_service = \
            Service( executable_path=selenium_conf["browser_driver"] )

        browser_opts = Options()
        for tmp_opt in selenium_conf["browser_options"]:
            browser_opts.add_argument( tmp_opt )

        browser = webdriver.Edge(service = browser_service,
                                 options = browser_opts )
        # 要素が見つかるまで、最大 ?秒 待つ
        browser.implicitly_wait( selenium_conf["implicitly_wait"] )
        return browser
