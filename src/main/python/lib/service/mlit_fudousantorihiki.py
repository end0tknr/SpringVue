#!python
# -*- coding: utf-8 -*-

from jeraconv import jeraconv
from psycopg2 import extras # for bulk insert
from bs4      import BeautifulSoup
from util.db  import Db

import appbase
import copy
import csv
import glob
import json
import os
import re
import tempfile
import unicodedata
import urllib.request
import zipfile
from service.city       import CityService
from selenium.webdriver.common.alert import Alert

download_host      = 'https://www.land.mlit.go.jp'
download_init_path = '/webland/servlet/DownloadServlet'
download_param_tmpl = '?TDK=99&SKC=99999&DLF=true&TTC-From=%s&TTC-To=%s'
download_zip_path_tmpl = '/webland/zip/All_%s_%s.zip'

download_year_quatar_min = 20181

col_filters = {"種類"                   :"shurui",
               "地域"                   :"chiiki",
               "都道府県名"             :"pref",
               "市区町村名"             :"city",
               "地区名"                 :"town",
               "最寄駅：名称"           :"station",
               "最寄駅：距離（分）"     :"from_station_min",
               "取引価格（総額）"       :"price",
               "間取り"                 :"plan",
               "面積（㎡）"             :"land_area_m2",
               "延床面積（㎡）"         :"floor_area_m2",
               "建築年"                 :"build_year",
               "建物の構造"             :"structure",
               "今後の利用目的"         :"new_usage",
               "都市計画"               :"youto_chiiki",
               "取引時点"               :"trade_year_q"}

re_compile_city         = re.compile("^.+郡(.+町)$")
re_compile_num          = re.compile("^(\d+)")
re_compile_trade_year_q = re.compile("^(\d+)年第(\d)四半期")


logger = appbase.AppBase().get_logger()


class MlitFudousanTorihikiService(appbase.AppBase):

    def __init__(self):
        pass
        

    def download_save_master(self):
        download_url_pairs = self.find_download_urls()
        util_db = Db()

        for url_pair in download_url_pairs:
            self.make_download_zip( url_pair[0] )
            csv_infos = self.download_master( url_pair[1] )

            for csv_info in csv_infos:
                # bulk insert
                util_db.save_tbl_rows(
                    "mlit_fudousantorihiki",
                    ["trade_year_q","shurui","chiiki","pref","city","town",
                     "station","from_station_min","price","plan",
                     "floor_area_m2","land_area_m2","build_year",
                     "structure","new_usage","youto_chiiki"],
                    csv_info[1] )


            
    def find_download_urls(self):
        downloadable_year_quatars = self.find_download_year_quatars()
        saved_year_quatars = self.get_saved_year_quatars()

        ret_datas = []
        
        for year_quatar in downloadable_year_quatars:
            if year_quatar in saved_year_quatars:
                continue

            download_param = download_param_tmpl % (year_quatar,year_quatar)
            url_1 = download_host + download_init_path + download_param
            download_zip_path = download_zip_path_tmpl % (year_quatar,year_quatar)
            url_2 = download_host + download_zip_path
            ret_datas.append( [url_1,url_2] )
            
        return ret_datas

    def get_saved_year_quatars(self):
        sql = """
SELECT
  trade_year_q
FROM mlit_fudousantorihiki
GROUP BY trade_year_q
ORDER BY trade_year_q

"""
        ret_datas = []
        
        db_conn = self.db_connect()
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute( sql )
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return []
            for ret_row in  db_cur.fetchall():
                ret_datas.append( dict( ret_row )["trade_year_q"])
        return ret_datas

        
    def find_download_year_quatars(self):
        # BeautifulSoup の方が安定していますが、urllib.request で
        # なぜか 「[Errno 104] Connection reset by peer」エラーとなる為、
        # selenium を使用しています
        browser = self.get_browser()
        req_url = download_host + download_init_path
        browser.get(req_url)
        
        opt_elms  = browser.find_elements_by_css_selector("#TDIDTo option")
        year_quarters = []
        for opt_elm in opt_elms:
            year_quarter = int( opt_elm.get_attribute("value") )
            if year_quarter < download_year_quatar_min:
                continue
            year_quarters.append( year_quarter )
            
        browser.close()
        year_quarters.sort()
        
        return year_quarters
        
    def make_download_zip(self, download_url):
        logger.info( download_url )

        browser = self.get_browser()
        browser.get( download_url )
        download_btns = browser.find_elements_by_css_selector("#download_button")
        if len( download_btns ) == 0:
            logger.error("not found download button "+download_url )
            return False

        # 以下の操作でサーバ側で zip が作成されます
        download_btns[0].click()
        Alert( browser ).accept()
        return True
    
    def download_master(self, download_url):
        logger.info( download_url )
        
        ret_data = []
    
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_zip_path =os.path.join(tmp_dir, "tmp.zip")

            data = self.get_http_requests( download_url )

            try:
                with open(tmp_zip_path, mode="wb") as fh:
                    fh.write(data)

                zip = zipfile.ZipFile(tmp_zip_path, "r")
                zip.extractall(path=tmp_dir)
                zip.close()

            except Exception as e:
                logger.error(e)
                logger.error(download_url)
                return []

            for csv_path in glob.glob(tmp_dir + '/*.csv' ):
                csv_name = str( os.path.split(csv_path)[1] )

                # csv.DictReader() での総行数の算出方法が不明でしたので。
                dict_row_size = len(open(csv_path,encoding='cp932').readlines() )

                with open(csv_path, encoding='cp932', newline="") as f:
                    # key-value形式での読込み
                    dict_reader = csv.DictReader(f, delimiter=",", quotechar='"')
                    new_rows = []
                    i = 0
                    for dict_row in dict_reader:
                        i += 1
                        if i % 10000 == 0:
                            logger.info( "%d/%d %s" % (i,dict_row_size,csv_path))
                            
                        new_row = {}
                        # tuple -> hashmap
                        for k, v in dict_row.items():
                            new_row[k] = v
                        # 行 & 列を選定
                        new_row = self.__filter_data(new_row)
                        if new_row:
                            new_rows.append( new_row )
                        
                    ret_data.append([csv_name, new_rows])

        return ret_data

    def __filter_data(self,org_row):
        
        ret_row = {}
        for org_key,new_key in col_filters.items():
            ret_row[new_key] = org_row[org_key]
            if len(ret_row[new_key]) == 0:
                ret_row[new_key] = None

        # 〇〇郡〇〇町 -> 〇〇町
        re_result = re_compile_city.search(ret_row["city"])
        if re_result:
            ret_row["city"] = re_result.group(1)
        
        # 全角->半角
        if ret_row["plan"]:
            ret_row["plan"] = unicodedata.normalize("NFKC", ret_row["plan"])
            
        # 例 2000㎡以上->2000
        for atri_key in ["land_area_m2","floor_area_m2","from_station_min"]:
            if not ret_row[atri_key]:
                continue
            re_result = re_compile_num.search(ret_row[atri_key])
            if re_result:
                ret_row[atri_key] = int( re_result.group(1) )
                
        # 例 2014年第４四半期->20144
        for atri_key in ["trade_year_q"]:
            if not ret_row[atri_key]:
                continue
            re_result = re_compile_trade_year_q.search( ret_row[atri_key] )
            if not re_result:
                continue
            
            ret_row[atri_key] = "%s%s" % (re_result.group(1),re_result.group(2))
            ret_row[atri_key] = int(ret_row[atri_key])
            
        if ret_row["build_year"]:
            if ret_row["build_year"] == "戦前":
                ret_row["build_year"] = None
            else:
                # 和暦 -> 西暦
                try:
                    ret_row["build_year"] = \
                        jeraconv.J2W().convert(ret_row["build_year"])
                except Exception as e:
                    logger.error(e)
                    logger.error( ret_row["build_year"] )


        for atri_key in ["from_station_min","price"]:
            
            if type( ret_row[atri_key] ) is str:
            
                if len(ret_row[atri_key])==0:
                    ret_row[atri_key] = None
                else:
                    ret_row[atri_key] = float(ret_row[atri_key])

        #print( ret_row )
                    
        return ret_row
            

    def get_vals_group_by_city(self):

        pre_year   = calc_filter["trade_year"] - 5
        pre_vals_tmp = self.get_tmp_vals_by_city( pre_year )

        pre_vals = {}
        for pre_val_tmp in pre_vals_tmp:
            pref_city = "\t".join([pre_val_tmp["pref"], pre_val_tmp["city"] ] )
            if not pref_city in pre_vals:
                pre_vals[pref_city] = {}
            
            shurui = pre_val_tmp["shurui"]
            pre_vals[pref_city][shurui + "_count"] = pre_val_tmp["count"]
            pre_vals[pref_city][shurui + "_price"] = pre_val_tmp["price"]


        now_vals_tmp = self.get_tmp_vals_by_city( calc_filter["trade_year"] )
        now_vals = {}
        for now_val_tmp in now_vals_tmp:
            
            pref_city = "\t".join([now_val_tmp["pref"], now_val_tmp["city"] ])
            if not pref_city in now_vals:
                now_vals[pref_city] = {"pref":now_val_tmp["pref"],
                                       "city":now_val_tmp["city"]}
            
            shurui = now_val_tmp["shurui"]
            for atri_key_tmp in ["count","price"]:
                atri_key = "%s_%s" %(shurui,atri_key_tmp)
                now_vals[pref_city][atri_key] = now_val_tmp[atri_key_tmp]
                
            
            if not pref_city in pre_vals:
                for atri_key_tmp in ["count","price"]:
                    atri_key = "%s_%s" %(shurui,atri_key_tmp)
                    now_vals[pref_city][atri_key+"_pre"] = 0
                continue

            for atri_key_tmp in ["count","price"]:
                atri_key = "%s_%s" %(shurui,atri_key_tmp)
                if not atri_key in pre_vals[pref_city]:
                    now_vals[pref_city][atri_key+"_pre"] = 0
                    continue
                
                now_vals[pref_city][atri_key+"_pre"] = \
                    pre_vals[pref_city][atri_key]
            
        return now_vals.values()
            
            
    def get_tmp_vals_by_city(self,trade_year):
        sql = """
select
  pref, city, trade_year, shurui,
  count(*) as count,
  avg(price)::numeric::bigint as price
from mlit_fudousantorihiki
where trade_year=%s AND shurui in %s
group by trade_year,pref,city,shurui
"""
        ret_data = []
        
        db_conn = self.db_connect()
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute(sql, (trade_year,calc_filter["shurui"]))
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return []
            for ret_row in  db_cur.fetchall():
                ret_data.append( dict( ret_row ))
        return ret_data
