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
    
    def __init__(self):
        pass
    

    def find_search_result_list_url(self):
        logger.info("start")
        
        for base_url in base_urls:
            for pref_name in pref_names:

                #他の都道府県のurl構成が異なる為、無視(skip)
                if pref_name == "hokkaido" and \
                     base_url == "https://suumo.jp/ms/shinchiku/":
                    continue
                
                #「hokkaido_」のように「_」が付加されている為
                if pref_name == "hokkaido" and \
                   base_url in ("https://suumo.jp/ikkodate/",
                                "https://suumo.jp/chukoikkodate/",
                                "https://suumo.jp/ms/chuko/"):
                    pref_name += "_"
                
                
                print("%s %s" %(base_url, pref_name))


    def find_search_result_list_url_sub(self, base_url, pref_name):
        logger.info("%s %s" % (base_url, pref_name))

        req_url = base_url + pref_name +"/city/"
        browser.get( req_url )

        # 検索ボタン click
        submit_btns = \
            browser.find_elements_by_css_selector(
                ".ui-btn--search"
            )

        if len(submit_btns) == 0:
            print("ERROR find_elements_by_css_selector() ",req_url, file=sys.stderr)
            sys.exit()
            return []

        submit_btns[0].click()
        time.sleep(2)

        paginations = []
        paginations.extend(
            browser.find_elements_by_css_selector(
                ".pagination.pagination_set-nav ol li")
        )
        paginations.extend(
            browser.find_elements_by_css_selector(
                ".sortbox_pagination ol li")
        )

        ret_urls = [browser.current_url]
        if len(paginations) == 0:
            return ret_urls

        for pno in range( 1, int(paginations[-1].text) ):
            ret_urls.append("%s&pn=%d" % (browser.current_url, pno+1) )

        return ret_urls
