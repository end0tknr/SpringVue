#!python
# -*- coding: utf-8 -*-

import appbase
import json
import re
import time
import urllib.parse
import urllib.request

conf = {
    "chrome_options" : [#"--headless",
                        "--enable-logging=False",
                        #以下、3行はSSLエラー対策らしい
                        "--ignore-certificate-errors",
                        "--disable-extensions",
                        "--disable-print-preview"],
    "implicitly_wait": 10 }

pref_names = [
    "hokkaido",
    "aomori","iwate","miyagi","akita","yamagata",
    "fukushima","ibaraki","tochigi",
    "gumma",            # suumo では、gunma でなく gumma
    "saitama","chiba","tokyo","kanagawa",
    "niigata","toyama","ishikawa","fukui","yamanashi","nagano","gifu",
    "shizuoka","aichi","mie","shiga","kyoto","osaka","hyogo","nara",
    "wakayama","tottori","shimane","okayama","hiroshima","yamaguchi",
    "tokushima","kagawa","ehime","kochi","fukuoka","saga","nagasaki",
    "kumamoto","oita","miyazaki", "kagoshima"
]
base_urls = [
    "https://suumo.jp/ikkodate/",       #新築戸建
    "https://suumo.jp/chukoikkodate/",  #中古戸建
    "https://suumo.jp/ms/shinchiku/",   #新築マンション
    "https://suumo.jp/ms/chuko/",       #中古マンション
]


logger = appbase.AppBase.get_logger()

class SuumoService(appbase.AppBase):
    
    def find_search_result_list_url(self):
        
        for base_url in base_urls:
            browser = init_browser(self)

    def init_browser():
        pass
