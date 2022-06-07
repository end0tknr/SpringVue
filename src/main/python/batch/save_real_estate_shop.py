#!python3
# -*- coding: utf-8 -*-

import getopt
import os
import sys
import re
import requests
import time
import urllib.parse

# http://chromedriver.chromium.org/getting-started
from selenium import webdriver # ex. pip install selenium==4.1.3
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

browser_conf = {
    "browser_driver": os.getcwd() + '\\chromedriver.exe',
    "browser_options" : [
        # "headless",
        "enable-logging=False",
        #以下はSSLエラー対策
        "ignore-certificate-errors",
        "disable-extensions",
        "ignore-ssl-errors",
        "disable-print-preview"],
    "implicitly_wait": 10 }


def main():

    url_base = "https://etsuran.mlit.go.jp/TAKKEN/takkenKensaku.do"
    pref_no = 12
    # pref_no = 13
    max_pref_no = 12
    # max_pref_no = 2

    while pref_no <= max_pref_no:
        req_url = url_base + "?dispCount=50&choice=1&kenCode=%02d" %(pref_no)
        print( "%s" % (req_url), file=sys.stderr )

        browser = init_browser()
        browser.get(req_url)

        search_btn = find_search_btn( browser )
        search_btn.click()
        
        shops_hash = parse_found_shops_pages(browser)

        for pref_licence,shop in shops_hash.items():
            print( pref_licence +"\t"+ shop )

        browser.close()
        pref_no += 1


def parse_found_shops_pages(browser):
    shops_hash = {}
    i = 0
    while(i < 50000 ):
        shops_hash_tmp = parse_shops( browser )
        shops_hash.update( shops_hash_tmp )

        select_elms = browser.find_elements(by=By.CSS_SELECTOR, value="#pageListNo1")
        page_no = Select(select_elms[0]).first_selected_option.text.split("/")

        if i % 10 == 0:
            print( "%s / %s" % (page_no[0],page_no[1]), file=sys.stderr )

        if page_no[0] == page_no[1]:
            break

        next_btn = find_next_btn( browser )
        next_btn.click()
        time.sleep(2)
        i += 1
        
    return shops_hash

def conv_shop_name(shop):
    replace_strs = ["株式会社","有限会社","合資会社","合同会社",'合名会社',
                    '独立行政法人','特定非営利活動法人','社会福祉法人',
                    '一般社団法人',"一般財団法人","公益財団法人"]
    for replace_str in replace_strs:
        shop = shop.replace(replace_str,"")

    shop = shop.strip().strip("　")
    return shop

def parse_shops( browser ):
    tr_elms = browser.find_elements(by=By.CSS_SELECTOR,value="table.re_disp tr")
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
        
        shop = conv_shop_name(shop)
        
        shop_key = government +"\t"+ licence
        shops_tmp[shop_key] = shop

    return shops_tmp
    
def find_search_btn( browser ):
    img_elms = browser.find_elements(by=By.CSS_SELECTOR, value="img")
    for img_elm in img_elms:
        img_src = img_elm.get_attribute("src")
        if img_src == "https://etsuran.mlit.go.jp/TAKKEN/images/btn_search_off.png":
            return img_elm
    return None


def find_next_btn( browser ):
    img_elms = browser.find_elements(by=By.CSS_SELECTOR, value="img")
    for img_elm in img_elms:
        img_src = img_elm.get_attribute("src")
        if img_src == "https://etsuran.mlit.go.jp/TAKKEN/images/result_move_r.jpg":
            return img_elm
    return None


def init_browser():
    browser_service = Service(
        executable_path=browser_conf["browser_driver"] )
    
    browser_opts = Options()
    for tmp_opt in browser_conf["browser_options"]:
        browser_opts.add_argument( tmp_opt )

    browser = webdriver.Chrome(service = browser_service,
                               options = browser_opts )
    # 要素が見つかるまで、最大 ?秒 待つ
    browser.implicitly_wait( browser_conf["implicitly_wait"] )
    return browser

if __name__ == '__main__':
    main()
