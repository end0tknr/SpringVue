#!python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from psycopg2  import extras # for bulk insert
from selenium import webdriver # ex. pip install selenium==4.1.3
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from util.db import Db

import appbase
import datetime
import json
import re
import time
import urllib.parse
import urllib.request

browser_conf = {
    "browser_options" : [
        "--headless",
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
    ["https://suumo.jp/ikkodate/",       "新築戸建"],
    ["https://suumo.jp/chukoikkodate/",  "中古戸建"],
    ["https://suumo.jp/ms/chuko/",       "中古マンション"],
    #新築マンションは価格等が記載されていないことが多い為、無視
    #["https://suumo.jp/ms/shinchiku/",  "新築マンション"]
]
disp_keys = [
    'base_url','物件名', '販売価格', '所在地','沿線・駅',
    '間取り','建物面積','専有面積','土地面積'
]
http_conf = {
    "retry_limit" : 10,
    "retry_sleep" : 10,
}

bulk_insert_size = 20
logger = None

class SuumoService(appbase.AppBase):
    
    def __init__(self):
        global logger
        logger = self.get_logger()

       
    def load_search_result_list_urls(self):
        logger.info("start")

        sql = "SELECT * FROM suumo_search_result_url"
        ret_rows = []

        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:

                    try:
                        db_cur.execute(sql)
                    except Exception as e:
                        logger.error(e)
                        logger.error(sql)
                        return []

                    for row in db_cur.fetchall():
                        ret_rows.append( [row["build_type"],row["url"]] )
                        #ret_rows.append( dict(row) )
        return ret_rows
    
    def save_bukken_infos(self, build_type, bukken_infos):
        logger.info("start "+ build_type)

        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        row_groups = self.divide_rows_info(build_type,
                                           bukken_infos,
                                           bulk_insert_size,
                                           date_str )

        sql = """
INSERT INTO suumo_bukken
  (build_type,bukken_name,price,price_org,address,plan,build_area_m2,
   build_area_org,land_area_m2,land_area_org,build_year,
   found_date)
  VALUES %s
ON CONFLICT ON CONSTRAINT suumo_bukken_pkey
  DO UPDATE SET check_date='%s'
"""
        sql = sql % ("%s", date_str)
        
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:

                for row_group in row_groups:
                    try:
                        # bulk insert
                        extras.execute_values(db_cur,sql, row_group )
                    except Exception as e:
                        logger.error(e)
                        logger.error(sql)
                        logger.error(row_group)
                        return False
                    
            db_conn.commit()
        return True
    
    def make_tuple_for_insert(self, build_type, org_row, date_str):
        
        ret_tuple = ( build_type                or "",
                      org_row['bukken_name']    or "",
                      org_row['price'],
                      org_row['price_org'],
                      org_row['address']        or "",
                      org_row['plan'],
                      org_row['build_area_m2'],
                      org_row['build_area_org'] or "",
                      org_row['land_area_m2'],
                      org_row['land_area_org']  or "",
                      org_row['build_year']     or 0,
                      date_str )
        tuple_key = "\t".join([ ret_tuple[0],
                                ret_tuple[1],
                                ret_tuple[4],
                                ret_tuple[7],
                                ret_tuple[9],
                                str( ret_tuple[10]) ] )
        return ret_tuple, tuple_key

        
    def divide_rows_info(self, build_type, org_rows, chunk_size,date_str):
        i = 0
        chunk = []
        ret_rows = []
        tuple_keys = {}
        for org_row in org_rows:
            
            org_tuple, tuple_key = self.make_tuple_for_insert(build_type,
                                                              org_row,
                                                              date_str)

            if tuple_key in tuple_keys:
                logger.warning("duplicate bukken "+ tuple_key)
                continue
            
            tuple_keys[tuple_key] = 1
            
            chunk.append( org_tuple )
            
            if len(chunk) >= chunk_size:
                ret_rows.append(chunk)
                chunk = []
            i += 1

        if len(chunk) > 0:
            ret_rows.append(chunk)

        return ret_rows
    
    def del_search_result_list_urls(self):
        logger.info("start")

        sql = "delete from suumo_search_result_url"

        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:
                try:
                    db_cur.execute(sql)
                except Exception as e:
                    logger.error(e)
                    logger.error(sql)
                    return False
                
            db_conn.commit()
            
        return True

        
    def save_search_result_list_urls(self, build_type, urls):
        logger.info("start "+ build_type)

        save_rows = []
        for url in urls:
            save_rows.append({"build_type":build_type,"url":url})

        util_db = Db()
        util_db.save_tbl_rows("suumo_search_result_url",
                              ["build_type","url"],
                              save_rows )


    def divide_rows_list(self, build_type, org_rows, chunk_size):
        i = 0
        chunk = []
        ret_rows = []
        for org_row in org_rows:
            chunk.append( (build_type, org_row) )
            
            if len(chunk) >= chunk_size:
                ret_rows.append(chunk)
                chunk = []
            i += 1

        if len(chunk) > 0:
            ret_rows.append(chunk)

        return ret_rows

        
    def find_search_result_list_url(self):
        logger.info("start")

        ret_urls = {}
        for base_url_tmp in base_urls:
            base_url   = base_url_tmp[0]
            build_type = base_url_tmp[1]
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
                if not build_type in ret_urls:
                    ret_urls[build_type] = []
                
                ret_urls[build_type].extend(tmp_urls)
                
        return ret_urls
    

    def find_search_result_list_url_sub(self, base_url, pref_name):
        logger.info("%s %s" % (base_url, pref_name))

        browser = self.get_browser()
        
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
    

    def get_http_requests(self, result_url):
        i = 0
        while i < http_conf["retry_limit"]:
            i += 1
            result = None
            try:
                html_content = urllib.request.urlopen(result_url).read()
                return html_content
            except:
                logger.warning("retry requests.get() " + result_url)
                time.sleep(http_conf["retry_sleep"])

        logger.error("requests.get() " + result_url)
        return None
    

    def parse_bukken_infos(self, result_list_url):
        logger.info("start " + result_list_url)

        html_content = self.get_http_requests( result_list_url )
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')

        bukken_divs = soup.select("div.dottable.dottable--cassette")
        
        ret_bukken_infos = []

        for bukken_div in bukken_divs:
            bukken_info = {}
            dls = bukken_div.select("dl")
            for dl in dls:
                dts = dl.select("dt")
                dds = dl.select("dd")
                if len(dts) == 0 or len(dds) == 0:
                    continue
                bukken_info[ dts[0].text.strip() ] = dds[0].text.strip()

            ret_bukken_infos.append( self.conv_bukken_info(bukken_info) )
        return ret_bukken_infos
    

    def conv_bukken_info(self,org_info):
        
        org_new_keys = {
            '物件名'  :'bukken_name',
            '販売価格':'price_org',
            '所在地'  :'address',
            '間取り'  :'plan',
            '土地面積':'land_area_org',
            '土地面積':'land_area_org',
            '築年月'  :'build_year'
        }
        ret_info = {}
        for org_key,new_key in org_new_keys.items():
            if not org_key in org_info:
                ret_info[new_key] = None
                continue
            ret_info[new_key] = org_info[org_key] or None

        for org_key in ["建物面積","専有面積"]:
            if org_key in org_info:
                ret_info["build_area_org"] = org_info[org_key]
        if not "build_area_org" in ret_info:
            ret_info["build_area_org"] = None

        ret_info["build_area_m2"] = self.conv_area( ret_info["build_area_org"] )
        ret_info["land_area_m2"]  = self.conv_area( ret_info["land_area_org"] )
        ret_info["price"]         = self.conv_price( ret_info["price_org"] )
        ret_info["build_year"]    = self.conv_build_year( ret_info["build_year"] )
        
        return ret_info
    

    def conv_area(self, org_val ):
        if not org_val or org_val == "-":
            return None

        # 中央値を返す
        re_compile_val_2 = \
            re.compile("([\d\.]{2,10})(?:m2|㎡).+?([\d\.]{2,10})(?:m2|㎡)")
        re_result = re_compile_val_2.search( org_val )
        if re_result:
            ret_val = float(re_result.group(1)) + float(re_result.group(2))
            return ret_val /2
        
        re_compile_val_1 = re.compile("([\d\.]{2,10})(?:m2|㎡)")
        re_result = re_compile_val_1.search( org_val )
        if re_result:
            ret_val = float(re_result.group(1))
            return ret_val

        logger.error( org_val )
        
        
    def conv_price(self, org_val ):
        if not org_val:
            return None
        if org_val in ["未定"]:
            return None

        # 中央値(万円)を返す
        re_compile_val_2 = \
            re.compile("([\d\.]{1,10})(万|億).+?([\d\.]{1,10})(万|億)")
        re_result = re_compile_val_2.search( org_val )
        if re_result:
            ret_val = (int(re_result.group(1)) + int(re_result.group(3))) /2
            if re_result.group(2) == "万":
                ret_val *= 10000
            elif re_result.group(2) == "億":
                ret_val *= 100000000
            return ret_val
        
        re_compile_val_1 = re.compile("([\d\.]{1,10})(万|億)")
        re_result = re_compile_val_1.search( org_val )
        if re_result:
            ret_val = int( re_result.group(1) )
        
            if re_result.group(2) == "万":
                ret_val *= 10000
            elif re_result.group(2) == "億":
                ret_val *= 100000000
            return ret_val

        logger.error( org_val )

    def conv_build_year(self, org_val ):
        if not org_val:
            return None

        re_compile_val_1 = re.compile("(\d\d\d\d)年")
        re_result = re_compile_val_1.search( org_val )
        if re_result:
            ret_val = int(re_result.group(1))
            return ret_val

        logger.error( org_val )

        
        
