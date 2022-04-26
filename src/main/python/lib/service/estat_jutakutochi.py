#!python
# -*- coding: utf-8 -*-

# refer urls are below.
# https://gigazine.net/news/20151201-household-income-map/
# https://gunmagisgeek.com/datavis/mimanCity/
# http://www.e-stat.go.jp/SG1/estat/NewList.do?tid=000001063455
# https://github.com/shimizu/H25_yearly_income

from bs4 import BeautifulSoup
from psycopg2  import extras # for bulk insert

import appbase
import copy
import json
import xlrd # for xls
import os
import re
import tempfile
import urllib.request
from service.city       import CityService

master_xls  = "b013.xls"
target_host = "http://www.e-stat.go.jp"
target_tbl_name = "".join([
    "家計を主に支える者の年齢(6区分)・従業上の地位(8区分)・",
    "世帯の年間収入階級(5区分)，",
    "現住居以外の土地の所有状況(4区分)別普通世帯数―市区町村"])
target_tbl_url = re.compile("^/stat-search/file-download")
bulk_insert_size = 20


logger = appbase.AppBase.get_logger()

class EstatJutakuTochiService(appbase.AppBase):

    def __init__(self):
        pass

    def save_tbl_rows(self, rows):
        logger.info("start")
        logger.info(rows[0])
        
        row_groups = self.__divide_rows(rows, bulk_insert_size)
        sql = """
INSERT INTO estat_jutakutochi (city,setai,setai_nushi_age,setai_year_income)
VALUES %s
 ON CONFLICT DO NOTHING
"""
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:

                for row_group in row_groups:
                    try:
                        # bulk insert
                        extras.execute_values(db_cur,sql,row_group)
                    except Exception as e:
                        logger.error(e)
                        logger.error(sql)
                        logger.error(row_group)
                        return False
                    
            db_conn.commit()
        return True
    

    def __divide_rows(self, org_rows, chunk_size):
        i = 0
        chunk = []
        ret_rows = []
        for org_row in org_rows:
            chunk.append( ( org_row['city'],
                            org_row['setai'],
                            json.dumps(org_row['setai_nushi_age'],
                                       ensure_ascii=False),
                            json.dumps(org_row['setai_year_income'],
                                       ensure_ascii=False) ) )
            
            if len(chunk) >= chunk_size:
                ret_rows.append(chunk)
                chunk = []
            i += 1

        if len(chunk) > 0:
            ret_rows.append(chunk)

        return ret_rows

    
    def download_excel(self, download_url):
        logger.info(download_url)
        
        ret_data = []
    
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_xls_path =os.path.join(tmp_dir, master_xls)
            try:
                data = urllib.request.urlopen(download_url).read()
                with open(tmp_xls_path, mode="wb") as fh:
                    fh.write(data)
                
                wbook = xlrd.open_workbook(tmp_xls_path)
                for sheetname in wbook.sheet_names():
                    wsheet = wbook.sheet_by_name(sheetname)
                    
                    logger.info("start %s %d rows" % (sheetname, wsheet.nrows) )

                    tmp_ret_data = self.__load_wsheet( wsheet )
                    ret_data.extend( tmp_ret_data )
                
            except Exception as e:
                logger.error("fail", download_url)
                logger.error(e)
                return []
            
        return ret_data
        
    def __load_wsheet( self, wsheet ):
        
        ret_data = []
        city_template = {"city":"",
                         "setai":0,
                         "setai_nushi_age"  :{}, #json
                         "setai_year_income":{}} #json
        now_city = None
        now_data = None
        row_no = 21
        
        while row_no < wsheet.nrows :
            tmp_atri_key = wsheet.cell_value(row_no,7)
            if not tmp_atri_key :
                row_no += 1
                continue

            tmp_atri_key = \
                tmp_atri_key.translate(str.maketrans({' ': '', '　': ''}))

            city_def = self.__is_city_caption(tmp_atri_key)
            if city_def:
                if now_city:
                    ret_data.append(now_city)
                now_city = copy.deepcopy( city_template )
                now_city["city"] = city_def["city"]
                row_no += 1
                continue

            if not now_city:
                row_no += 1
                continue

            if tmp_atri_key == "普通世帯総数":
                now_city["setai"] = wsheet.cell_value(row_no,10)
                row_no += 1
                continue
            if tmp_atri_key == "(その１.家計を主に支える者の年齢)":
                now_data = "setai_nushi_age"
                row_no += 1
                continue
            if tmp_atri_key == "(その２.従業上の地位)":
                now_data = None
                row_no += 1
                continue
            if tmp_atri_key == "(その３.世帯の年間収入階級)":
                now_data = "setai_year_income"
                row_no += 1
                continue
            if not now_data:
                row_no += 1
                continue

            now_city[now_data][tmp_atri_key] = wsheet.cell_value(row_no,10)
            row_no += 1
        return ret_data
            
    def __is_city_caption(self, tmp_atry_key):
        re_compile = re.compile("(\d+)([^%d]+)")
        re_result = re_compile.search(tmp_atry_key)
        if not re_result:
            return None

        city_code = re_result.group(1)
        city_tmp  = re_result.group(2)

        city_service = CityService()
        return city_service.find_def_by_code_city( city_code, city_tmp )

    def __find_pref_links(self, hrefs):
        ret_urls = []
        
        re_compile = re.compile("([^\d]+[都道府県]).+2\d\d件")
        for href in hrefs:
            href_text = href.text.replace('\n', '').strip()

            re_result = re_compile.search(href_text)
            if not re_result:
                continue
            
            ret_urls.append( [re_result.group(1),
                              target_host+ href.attrs['href'] ])
        return ret_urls
            
        
    def __find_download(self, pref_req_url ):

        html_content = urllib.request.urlopen(pref_req_url).read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tmp_css_selector = ".stat-dataset_list-item"
        articles = []
        try:
            articles = soup.select(tmp_css_selector)
        except Exception as e:
            logger.error(e)
            logger.error(pref_req_url)
            return ""

        for article in articles:
            download_url = self.__find_download_sub( article )
            if download_url:
                return download_url
            
    def __find_download_sub(self, elm_article ):
        elm_lis = []
        tmp_css_selector = ".stat-dataset_list-detail-item"
        try:
            elm_lis = elm_article.select(tmp_css_selector)
        except Exception as e:
            logger.error(e)
            return ""
        
        if len(elm_lis)==0:
            return ""
        
        tmp_text = elm_lis[0].text.replace('\n', '').strip()
        re_compile = re.compile("111") #= 表番号
        if not re_compile.search(tmp_text):
            return ""
                
        tmp_css_selector = ".stat-link_text"
        try:
            elm_lis = elm_article.select(tmp_css_selector)
        except Exception as e:
            logger.error(e)
            return ""

        tmp_text = elm_lis[0].text.replace('\n', '').strip()
            
        if tmp_text != target_tbl_name:
            return ""

        hrefs = []
        try:
            hrefs = elm_article.select("a")
        except Exception as e:
            logger.error(e)
            return ""

        re_compile = re.compile(target_tbl_url)
        
        for href in hrefs:
            download_url = href.attrs['href']

            if re_compile.search(download_url):
                return target_host + download_url

            
    def find_download_urls(self):
        logger.info("start")
        
        req_url = target_host+ '/SG1/estat/NewList.do?tid=000001063455'
        html_content = urllib.request.urlopen(req_url).read()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        tmp_css_selector = ".stat-matter3 a"
        try:
            hrefs = soup.select(tmp_css_selector)
        except Exception as e:
            logger.error(e)
            logger.error(req_url)
            return []

        pref_urls = self.__find_pref_links(hrefs)

        ret_urls = []
        for pref_url in pref_urls:
            logger.info("start "+pref_url[0]+" "+ pref_url[1])
            ret_url = self.__find_download(pref_url[1] )
            logger.info("done "+pref_url[0]+" "+ ret_url)

            ret_urls.append( ret_url )
            
        return ret_urls
