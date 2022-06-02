#!python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from psycopg2  import extras # for bulk insert
from selenium import webdriver # ex. pip install selenium==4.1.3
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from service.city  import CityService
from util.db import Db

import appbase
import datetime
import json
import re
import sys
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
    "hokkaido","aomori","iwate","miyagi","akita","yamagata",
    "fukushima","ibaraki","tochigi",
    "gumma",            # suumo では、gunma でなく gumma
    "saitama","chiba",
    "tokyo",
    "kanagawa",
    "niigata","toyama","ishikawa","fukui","yamanashi","nagano","gifu",
    "shizuoka","aichi","mie","shiga","kyoto","osaka","hyogo","nara",
    "wakayama","tottori","shimane","okayama","hiroshima","yamaguchi",
    "tokushima","kagawa","ehime","kochi","fukuoka","saga","nagasaki",
    "kumamoto","oita","miyazaki", "kagoshima"
]

base_host = "https://suumo.jp"
base_urls = [
    [base_host+"/ikkodate/",       "新築戸建"],
    # [base_host+"/chukoikkodate/",  "中古戸建"],
    # [base_host+"/ms/chuko/",       "中古マンション"],
    # 新築マンションは価格等が記載されていないことが多い為、無視
    #[base_host+"/ms/shinchiku/",  "新築マンション"]
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


    def modify_pref_city(self,address_org,pref,city,other):
        sql = """
UPDATE suumo_bukken
SET pref=%s, city=%s, address=%s
WHERE address=%s
"""
        sql_args = (pref,city,other,address_org)
        
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:
                try:
                    db_cur.execute(sql,sql_args)
                    db_conn.commit()
                except Exception as e:
                    logger.error(e)
                    logger.error(sql)
                    return False

        return True
        
    def load_all_bukkens(self):
        ret_rows = []
        sql = """
SELECT * FROM suumo_bukken where pref =''
"""
        
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:
                try:
                    db_cur.execute(sql)
                except Exception as e:
                    logger.error(e)
                    logger.error(sql)
                    return []

                ret_rows = db_cur.fetchall()
                
        for ret_row in ret_rows:
            ret_row = dict( ret_row )
            
        return ret_rows
        
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
    
    def save_bukken_infos_main(self):
        logger.info("start")
        
        # 物件一覧のurl探索
        result_list_urls = self.find_search_result_list_url()
        # 物件一覧の旧url 削除
        self.del_search_result_list_urls()

        # 物件一覧の新url 登録
        for build_type, result_list_urls in result_list_urls.items():
            self.save_search_result_list_urls(build_type,result_list_urls)
            
        # 物件一覧の新url 再? load
        result_list_urls = self.load_search_result_list_urls()
            
        # 各物件情報の取得と保存
        i = 0
        for result_list_tmp in result_list_urls:
            i += 1
            build_type      = result_list_tmp[0]
            result_list_url = result_list_tmp[1]

            if i % 20 == 0:
                logger.info("%d/%d %s %s" % (i,len(result_list_urls),
                                             build_type,
                                             result_list_url ))
            
            bukken_infos = self.parse_bukken_infos(result_list_url)
            self.save_bukken_infos(build_type,bukken_infos)

        
    def save_bukken_infos(self, build_type, bukken_infos):

        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        row_groups = self.divide_rows_info(build_type,
                                           bukken_infos,
                                           bulk_insert_size,
                                           date_str )

        sql = """
INSERT INTO suumo_bukken
  (build_type,bukken_name,price,price_org,pref,city,address,
   plan,build_area_m2,build_area_org,land_area_m2,land_area_org,
   build_year,shop_org,url,found_date,check_date)
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
                      org_row['pref']           or "",
                      org_row['city']           or "",
                      org_row['address']        or "",
                      org_row['plan'],
                      org_row['build_area_m2'],
                      org_row['build_area_org'] or "",
                      org_row['land_area_m2'],
                      org_row['land_area_org']  or "",
                      org_row['build_year']     or 0,
                      org_row['shop_org'],
                      org_row['url'],
                      date_str,
                      date_str )
        tuple_key = "\t".join([ ret_tuple[0],
                                ret_tuple[1],
                                ret_tuple[4],
                                ret_tuple[5],
                                ret_tuple[6],
                                ret_tuple[9],
                                ret_tuple[11],
                                str( ret_tuple[12]) ] )
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
                logger.debug("duplicate bukken "+ tuple_key)
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

        html_content = self.get_http_requests( result_list_url )
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        
        ret_bukken_infos = []
        bukken_parent_divs = soup.select("div.property_unit-content")
        # bukken_divs = soup.select("div.dottable.dottable--cassette")
        
        for bukken_div in bukken_parent_divs:
            bukken_info = {}
            bukken_info["url"] = self.parse_bukken_url(bukken_div)
            
            dls = bukken_div.select("dl")
            for dl in dls:
                dts = dl.select("dt")
                dds = dl.select("dd")
                if len(dts) == 0 or len(dds) == 0:
                    continue
                bukken_info[ dts[0].text.strip() ] = dds[0].text.strip()

            bukken_info["shop_org"] = self.find_shop_name( bukken_div,
                                                           bukken_info["url"] )
            ret_bukken_infos.append( self.conv_bukken_info(bukken_info) )
        return ret_bukken_infos
    
    
    def parse_bukken_url(self, bukken_div):
        a_elms = bukken_div.select(".property_unit-title a")
        if not len(a_elms):
            return None

        re_compile = re.compile("href=[\"\']?([^\s\"\']+)[\"\']?")
        re_result = re_compile.search( str(a_elms[0]) )
        if not re_result:
            return None

        bukken_detail_url = base_host+re_result.group(1)
        return bukken_detail_url

        
    def find_shop_name(self, bukken_div, bukken_url ):

        divs = bukken_div.select("div.shopmore-title")
        if not len(divs):
            return None
        
        shop_org = self.parse_shop_name( divs[0].text.strip() )
        if shop_org:
            return shop_org

        return None

        # html_content = self.get_http_requests(bukken_url)
        # if not html_content:
        #     return None

        # soup = BeautifulSoup(html_content, 'html.parser')
        # contact_tos = soup.select("td.bdGrayB")
        # contact_to_str = contact_tos[0].text.strip()
        # shop_name_org = contact_to_str.split("\n")[0]
        # shop_name = self.parse_shop_name( shop_name_org )
        # return shop_name
        
    # def find_shop_name(self, bukken_div, bukken_url ):

    #     divs = bukken_div.select("div.shopmore-title")
    #     shop_org = self.parse_shop_name( divs[0].text.strip() )
    #     if shop_org:
    #         return shop_org

    #     html_content = self.get_http_requests(bukken_url)
    #     if not html_content:
    #         return None

    #     soup = BeautifulSoup(html_content, 'html.parser')
    #     contact_tos = soup.select("td.bdGrayB")
    #     contact_to_str = contact_tos[0].text.strip()
    #     shop_name_org = contact_to_str.split("\n")[0]
    #     shop_name = self.parse_shop_name( shop_name_org )
    #     return shop_name
        

    def parse_shop_name(self, org_shop_name):
        kabu_re_exp = "(?:株式会社|有限会社|\(株\)|\（株\）|\(有\)|\（有\）)"
        shp_re_exp  = "([^ 　\s\(\)（）]+)"
        
        if not org_shop_name:
            return None
        # 後株
        re_compile = re.compile( "^"+ shp_re_exp + kabu_re_exp )
        re_result = re_compile.search(org_shop_name)
        if re_result:
            return re_result.group(1)
        # 前株
        re_compile = re.compile( kabu_re_exp + shp_re_exp + "$" )
        re_result = re_compile.search(org_shop_name)
        if re_result:
            return re_result.group(1)

        return org_shop_name
    
    def conv_bukken_info(self,org_info):
        
        org_new_keys = {
            '物件名'  :'bukken_name',
            '販売価格':'price_org',
            '所在地'  :'address',
            '間取り'  :'plan',
            '土地面積':'land_area_org',
            '土地面積':'land_area_org',
            '築年月'  :'build_year',
            'url'     :'url',
            'shop_org':'shop_org',
        }
        ret_info = {}
        for org_key,new_key in org_new_keys.items():
            if not org_key in org_info:
                ret_info[new_key] = None
                continue
            ret_info[new_key] = org_info[org_key] or None

        address_org = ret_info["address"]
        city_service  = CityService()
        address_new = city_service.parse_pref_city(address_org)
        ret_info["pref"]    = address_new[0]
        ret_info["city"]    = address_new[1]
        ret_info["address"] = address_new[2]

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

        # 「???円～???円」表記の場合、中央値(万円)を返す
        re_compile_val_1 = \
            re.compile("([\d\.]{1,10})(万|億)[^\d]+?([\d\.]{1,10})(万|億)")
        re_result = re_compile_val_1.search( org_val )
        if re_result:
            ret_val = (int(re_result.group(1)) + int(re_result.group(3))) /2
            if re_result.group(2) == "万":
                ret_val *= 10000
            elif re_result.group(2) == "億":
                ret_val *= 100000000
            return ret_val

        re_compile_val_2 = re.compile("([\d\.]{1,5})億([\d\.]{1,5})万")
        re_result = re_compile_val_2.search( org_val )
        if re_result:
            ret_val =  int( re_result.group(1) ) * 100000000 # 億
            ret_val += int( re_result.group(2) ) * 10000     # 万
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

        
    def get_vals_group_by_city_sub(self, start_date_str, end_date_str):
        sql = """
select
  pref, city, build_type,
  count(*) as count,
  round(avg(price))::bigint as price
from suumo_bukken
where
  (check_date between %s AND %s)
group by pref,city,build_type
order by build_type, count(*) desc
"""
        ret_data_tmp = {}
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:
                try:
                    db_cur.execute(sql, (start_date_str, end_date_str))
                except Exception as e:
                    logger.error(e)
                    logger.error(sql)
                    return []

                for ret_row in  db_cur.fetchall():
                    ret_row= dict( ret_row )
                    pref_city = "%s\t%s" % (ret_row['pref'],ret_row['city'])
                    
                    if not pref_city in ret_data_tmp:
                        ret_data_tmp[pref_city] = {}
                        
                    build_type = ret_row['build_type']
                    ret_data_tmp[pref_city][build_type+"_count"]=ret_row['count']
                    ret_data_tmp[pref_city][build_type+"_price"]=ret_row['price']
                    
        ret_data = []
        for pref_city_str,key_vals in ret_data_tmp.items():
            pref_city = pref_city_str.split("\t")
            key_vals["pref"] = pref_city[0]
            key_vals["city"] = pref_city[1]
            ret_data.append(key_vals)

                
        return ret_data
    
    def get_last_check_date(self):
        sql = """
select
  check_date
from suumo_bukken
order by check_date desc
limit 1
"""
        ret_data_tmp = {}
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:
                try:
                    db_cur.execute(sql)
                except Exception as e:
                    logger.error(e)
                    logger.error(sql)
                    return None

                ret_row = db_cur.fetchone()
                return ret_row[0]
        
    def get_stock_vals(self):
        check_date = self.get_last_check_date()
        check_date_str = check_date.strftime('%Y-%m-%d')

        return self.get_vals_group_by_city_sub(check_date_str,check_date_str)

    def get_sold_vals(self):
        check_date = self.get_last_check_date()
        end_date = check_date + datetime.timedelta(days= -1)
        end_date_str = end_date.strftime('%Y-%m-%d')
        start_date_str = end_date.strftime('%Y-%m-01')

        return self.get_vals_group_by_city_sub(start_date_str,end_date_str)

