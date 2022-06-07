#!python
# -*- coding: utf-8 -*-

from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import Select
from util.db import Db

import appbase
import os
import jaconv        # pip install jaconv
import re
import time
import unicodedata   # 標準module
import urllib.request

url_base    = "https://etsuran.mlit.go.jp/TAKKEN/takkenKensaku.do"
insert_cols = ["government","licence","shop"]
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
        
    # selenium の headless modeでは動作しないみたい...
    def download_and_save_master(self):
        logger.info("start")

        pref_no     = 1
        max_pref_no = 47 # 47都道府県

        while pref_no <= max_pref_no:
            req_url = url_base + "?dispCount=50&choice=1&kenCode=%02d" %(pref_no)
            logger.info(req_url)

            browser = self.get_browser()
            browser.get(req_url)

            search_btn = self.find_search_btn( browser )
            search_btn.click()
            
            # parseした不動産会社情報のdb保存
            shops = self.parse_found_shops_pages(browser)
            self.save_tbl_rows(shops)

            browser.close()
            pref_no += 1

    def parse_found_shops_pages(self, browser):
        shops_hash = {}
        i = 0
        while(i < 1000 ):  # 1000は 最終pageを判定できない場合に備えたもの
            shops_hash_tmp = self.parse_shops( browser )
            shops_hash.update( shops_hash_tmp )

            select_elms = browser.find_elements(by=By.CSS_SELECTOR, value="#pageListNo1")
            page_no = Select(select_elms[0]).first_selected_option.text.split("/")

            if i % 10 == 0:
                logger.info("%s/%s %s" % (page_no[0],page_no[1],browser.current_url) )
            
            if page_no[0] == page_no[1]:  #最終pageに達したら、終了
                break

            next_btn = self.find_next_btn( browser )
            next_btn.click()
            time.sleep(2)
            i += 1

        ret_datas = []
        for pref_licence_str,shop in shops_hash.items():
            pref_licence = pref_licence_str.split("\t")
            ret_datas.append({"pref"    : pref_licence[0],
                              "licence" : pref_licence[1],
                              "shop"    : shop} )
        return ret_datas


    def conv_shop_name(self, shop):
        replace_strs = ["株式会社","有限会社","合資会社","合同会社",'合名会社',
                        '独立行政法人','特定非営利活動法人','社会福祉法人',
                        '一般社団法人',"一般財団法人","公益財団法人"]
        for replace_str in replace_strs:
            shop = shop.replace(replace_str,"")

        shop = shop.strip().strip("　")

        # 英数字とカナを半角化
        shop = unicodedata.normalize("NFKC", shop)
        shop = jaconv.z2h(shop, kana=True, ascii=False, digit=False)
        
        return shop

    def parse_shops( self, browser ):
        tr_elms = browser.find_elements(by=By.CSS_SELECTOR,value="table.re_disp tr")
        
        if len(tr_elms) == 0:
            logger.error("fail parse table.re_disp tr %s" % (browser.current_url))
            return []
        
        tr_elms.pop(0) # 先頭行はヘッダの為、削除

        re_compile = re.compile("[\(（].+[\)）]")

        shops_tmp = {}
        for tr_elm in tr_elms:
            cols_str = tr_elm.text
            cols = tr_elm.text.split(" ")

            government = "";
            licence    = "";
            shop       = "";

            if len(cols) == 7:
                government = re_compile.sub('',cols[1])
                licence    = re_compile.sub('',cols[2])
                shop = cols[3]
            elif len(cols) == 6:    #信託銀行の場合
                government = "-"
                licence    = re_compile.sub('',cols[1])
                shop       = cols[2]
            else:
                continue

            shop = self.conv_shop_name(shop)

            shop_key = government +"\t"+ licence
            shops_tmp[shop_key] = shop

        return shops_tmp

    def find_search_btn( self, browser ):
        img_elms = browser.find_elements(by=By.CSS_SELECTOR, value="img")
        for img_elm in img_elms:
            img_src = img_elm.get_attribute("src")
            if "btn_search_off.png" in img_src:
                return img_elm
        return None

    def find_next_btn( self, browser ):
        img_elms = browser.find_elements(by=By.CSS_SELECTOR, value="img")
        for img_elm in img_elms:
            img_src = img_elm.get_attribute("src")
            if "result_move_r.jpg" in img_src:
                return img_elm
        return None
            
