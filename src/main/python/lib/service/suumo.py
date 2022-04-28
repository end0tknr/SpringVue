#!python
# -*- coding: utf-8 -*-

from selenium import webdriver # ex. pip install selenium==4.1.3
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import appbase
import json
import re
import time
import urllib.parse
import urllib.request

browser_conf = {
    "browser_options" : [
        #"--headless",
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

        ret_urls = []
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
                
                tmp_urls = self.find_search_result_list_url_sub(base_url,
                                                                pref_name)
                ret_urls.extend(tmp_urls)
        return ret_urls
    

    def find_search_result_list_url_sub(self, base_url, pref_name):
        logger.info("%s %s" % (base_url, pref_name))
        browser = self.init_browser()
        
        req_url = base_url + pref_name +"/city/"
        browser.get( req_url )
        
        # 検索ボタン click
        css_selector = ".ui-btn--search"
        submit_btns = \
            browser.find_elements_by_css_selector(css_selector)

        if len(submit_btns) == 0:
            logger.error(req_url +" "+css_selector)
            browser.close()
            return []

        submit_btns[0].click()
        time.sleep(3)

        paginations = []
        paginations.extend(
            browser.find_elements_by_css_selector(
                ".pagination.pagination_set-nav ol li") )
        paginations.extend(
            browser.find_elements_by_css_selector(
                ".sortbox_pagination ol li") )

        ret_urls = [browser.current_url]
        if len(paginations) == 0:
            return ret_urls

        for pno in range( 1, int(paginations[-1].text) ):
            ret_urls.append("%s&pn=%d" % (browser.current_url, pno+1) )

        browser.close()
        return ret_urls


    def init_browser(self):
        driver_path = self.get_conf()["common"]["browser_driver"]
        browser_service = Service( executable_path=driver_path )

        browser_opts = Options()
        for tmp_opt in browser_conf["browser_options"]:
            browser_opts.add_argument( tmp_opt )

        browser = webdriver.Edge(service = browser_service,
                                 options = browser_opts )
        # 要素が見つかるまで、最大 ?秒 待つ
        browser.implicitly_wait( browser_conf["implicitly_wait"] )
        return browser
