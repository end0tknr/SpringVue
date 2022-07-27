#!python
# -*- coding: utf-8 -*-

from functools import cmp_to_key
from jeraconv import jeraconv
from psycopg2 import extras # for bulk insert
from bs4      import BeautifulSoup
from util.db  import Db
import operator
import appbase
import copy
import csv
import datetime
import glob
import json
import operator
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

    # https://www.land.mlit.go.jp/webland/download.html で
    # 公開済(= ダウンロード可能)なデータと
    # 既にDB保存されているデータを比較し
    # 未保存なデータのみ、ダウンロード & 保存します
    def find_download_urls(self):
        downloadable_year_quatars = self.find_download_year_quatars()
        saved_year_quatars = self.get_saved_year_quatars()

        ret_datas = []
        
        for year_quatar in downloadable_year_quatars:
            if year_quatar in saved_year_quatars:
                continue

            download_param = download_param_tmpl % (year_quatar,year_quatar)
            url_1 = download_host + download_init_path + download_param
            download_zip_path = download_zip_path_tmpl % (year_quatar,
                                                          year_quatar)
            url_2 = download_host + download_zip_path
            ret_datas.append( [url_1,url_2] )
            
        return ret_datas
    

    def get_saved_year_quatars(self,limit_year_q=0):
        sql = """
SELECT
  trade_year_q
FROM mlit_fudousantorihiki
WHERE trade_year_q >= %s
GROUP BY trade_year_q
ORDER BY trade_year_q
"""
        ret_datas = []
        
        db_conn = self.db_connect()
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute( sql,(limit_year_q,) )
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return []
            for ret_row in  db_cur.fetchall():
                ret_datas.append( dict( ret_row )["trade_year_q"])
        return ret_datas
    

    def get_city_summaries(self, atri_key_header, year_quatars ):
        sql = """
SELECT *
FROM mlit_fudousantorihiki_by_city
ORDER BY pref,city
"""
        ret_datas = []
        ret_datas_tmp = []
        
        db_conn = self.db_connect()
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute( sql )
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return []

            for ret_row in db_cur.fetchall():
                ret_row = dict( ret_row )
                tmp_summary = []
                if ret_row["summary"]:
                    tmp_summary = json.loads( ret_row["summary"] )
                    
                tmp_summaries = self.sort_select_summary(tmp_summary,
                                                         year_quatars[0],
                                                         year_quatars[-1],
                                                         1)
                count_key = atri_key_header+"_sold_count"
                price_key = atri_key_header+"_sold_price"
                if len(tmp_summaries):
                    ret_datas.append({
                        "pref" : ret_row["pref"],
                        "city" : ret_row["city"],
                        "sold_count" : tmp_summaries[0][count_key],
                        "sold_price" : tmp_summaries[0][price_key] })
                else:
                    ret_datas.append({
                        "pref" : ret_row["pref"],
                        "city" : ret_row["city"],
                        "sold_count" : 0,
                        "sold_price" : 0 })
                    
        return ret_datas
    

    def get_town_sumed_summaries(self, atri_key_header, year_quatars ):
        sql = """
SELECT *
FROM mlit_fudousantorihiki_by_town
ORDER BY pref,city,town
"""
        ret_datas = []
        ret_datas_tmp = []
        
        db_conn = self.db_connect()
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute( sql )
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return []

            for ret_row in db_cur.fetchall():
                ret_row = dict( ret_row )
                tmp_summaries = []
                if ret_row["summary"]:
                    tmp_summaries = json.loads( ret_row["summary"] )

                tmp_summaries = self.sort_select_summary(tmp_summaries,
                                                         year_quatars[0],
                                                         year_quatars[-1],
                                                         4)
                count = 0
                price = 0
                count_key = atri_key_header+"_sold_count"
                price_key = atri_key_header+"_sold_price"
                
                for tmp_summary in tmp_summaries:
                    quatar_count = tmp_summary[count_key] *12
                    count += quatar_count
                    price += ( tmp_summary[price_key] * quatar_count )
                    
                if count:
                    price /= count
                    
                ret_datas.append({
                    "pref" : ret_row["pref"],
                    "city" : ret_row["city"],
                    "town" : ret_row["town"],
                    "sold_count" : round(count),
                    "sold_price" : round(price) })
        return ret_datas
    

    def get_city_sumed_summaries(self, atri_key_header, year_quatars ):
        sql = """
SELECT *
FROM mlit_fudousantorihiki_by_city
ORDER BY pref,city
"""
        ret_datas = []
        ret_datas_tmp = []
        
        db_conn = self.db_connect()
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute( sql )
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return []

            for ret_row in db_cur.fetchall():
                ret_row = dict( ret_row )
                tmp_summaries = []
                if ret_row["summary"]:
                    tmp_summaries = json.loads( ret_row["summary"] )

                tmp_summaries = self.sort_select_summary(tmp_summaries,
                                                         year_quatars[0],
                                                         year_quatars[-1],
                                                         4)
                count = 0
                price = 0
                count_key = atri_key_header+"_sold_count"
                price_key = atri_key_header+"_sold_price"
                
                for tmp_summary in tmp_summaries:
                    quatar_count = tmp_summary[count_key] *12
                    count += quatar_count
                    price += ( tmp_summary[price_key] * quatar_count )
                    
                if count:
                    price /= count
                    
                ret_datas.append({
                    "pref" : ret_row["pref"],
                    "city" : ret_row["city"],
                    "sold_count" : round(count),
                    "sold_price" : round(price) })
        return ret_datas
    

    def sort_select_summary(self,summaries,cmp_key_min,cmp_key_max,limit):
        ret_datas = []
        cmp_key = "sold_trade_year_q"

        for summary in sorted(summaries, key=operator.itemgetter(cmp_key) ):
            if summary[cmp_key]<cmp_key_min or cmp_key_max<summary[cmp_key]:
                continue

            ret_datas.append(summary)
            if len(ret_datas) >= limit:
                break
        return ret_datas
    

    def get_town_summaries(self,atri_key_header, year_quatars ):
        sql = """
SELECT *
FROM mlit_fudousantorihiki_by_town
ORDER BY pref,city,town
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
                ret_row = dict( ret_row )
                tmp_summary = []
                if ret_row["summary"]:
                    tmp_summary = json.loads( ret_row["summary"] )

                tmp_summaries = self.sort_select_summary(tmp_summary,
                                                         year_quatars[0],
                                                         year_quatars[-1],
                                                         1)
                count_key = atri_key_header+"_sold_count"
                price_key = atri_key_header+"_sold_price"
                if len(tmp_summaries):
                    ret_datas.append({
                        "pref" : ret_row["pref"],
                        "city" : ret_row["city"],
                        "town" : ret_row["town"],
                        "sold_count" : tmp_summaries[count_key],
                        "sold_price" : tmp_summaries[price_key] })
                else:
                    ret_datas.append({
                        "pref" : ret_row["pref"],
                        "city" : ret_row["city"],
                        "town" : ret_row["town"],
                        "sold_count" : 0,
                        "sold_price" : 0 })
        return ret_datas

        
    def get_city_price_summaries(self,atri_key_header, year_quatars ):
        sql = """
SELECT *
FROM mlit_fudousantorihiki_by_city
ORDER BY pref,city
"""
        ret_datas = []
        re_compile = re.compile("_sold_price_m_(\d+)_count")
        
        db_conn = self.db_connect()
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute( sql )
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return []
            

            for ret_row in  db_cur.fetchall():
                ret_row = dict( ret_row )
                tmp_summary = []
                if ret_row["summary"]:
                    tmp_summary = json.loads( ret_row["summary"] )

                tmp_summary = self.sort_select_summary(tmp_summary,
                                                       year_quatars[0],
                                                       year_quatars[-1],
                                                       1)
                for atri_key in tmp_summary.keys():
                    re_result = re_compile.search( atri_key )
                    if not re_result:
                        continue

                    price_m = re_result.group(1)
                    sold_count = year_quatar_summary[atri_key]
                        
                    ret_datas.append({
                        "pref" : ret_row["pref"],
                        "city" : ret_row["city"],
                        "price": price_m,
                        "sold_count" : sold_count })
        return ret_datas
    
    
    def find_download_year_quatars(self):
        # BeautifulSoup の方が安定していますが、urllib.request で
        # なぜか 「[Errno 104] Connection reset by peer」エラーとなる為、
        # selenium を使用しています
        browser = self.get_browser()
        req_url = download_host + download_init_path
        browser.get(req_url)
        
        opt_elms  = browser.find_elements_by_css_selector("#TDIDTo option")
        year_quaters = []
        for opt_elm in opt_elms:
            year_quater = int( opt_elm.get_attribute("value") )
            if year_quater < download_year_quatar_min:
                continue
            year_quaters.append( year_quater )
            
        browser.close()
        year_quaters.sort()
        
        return year_quaters
        
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

        return ret_row
    

    def calc_save_summary( self ):
        self.calc_save_city_summary()
        self.calc_save_town_summary()
    
        
    def calc_save_city_summary( self ):
        util_db = Db()
        # 市区町村単位
        city_summuries_hash = self.calc_summary( ["pref","city"] )
        city_summuries     = self.conv_summary_to_list( city_summuries_hash )

        util_db.bulk_upsert( "mlit_fudousantorihiki_by_city",
                             ["pref","city"],
                             ["pref","city","summary"],
                             ["summary"],
                             city_summuries )
        

    def calc_save_town_summary( self ):
        util_db = Db()
        # 地区単位
        town_summuries_hash = self.calc_summary( ["pref","city","town"] )
        town_summuries     = self.conv_summary_to_list( town_summuries_hash )

        util_db.bulk_upsert( "mlit_fudousantorihiki_by_town",
                             ["pref","city","town"],
                             ["pref","city","town","summary"],
                             ["summary"],
                             town_summuries )


    def calc_summary( self, pkeys ):
        year = datetime.datetime.today().date().year - 1
        limit_year_q = int( "%s1" % (year,))
        
        year_quaters = self.get_saved_year_quatars(limit_year_q)
        
        sql = """
SELECT *
FROM mlit_fudousantorihiki
WHERE shurui='宅地(土地と建物)' AND new_usage='住宅' AND
      trade_year_q >= %s
ORDER BY pref,city,trade_year_q
"""
        
        ret_datas_tmp       = {}

        db_conn = self.db_connect()

        re_compile = re.compile("^(.+)\d")
        
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute( sql,(limit_year_q,) )
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return []

            for ret_row in  db_cur.fetchall():
                ret_row = dict( ret_row )

                town = ret_row["town"]
                if "town" in pkeys:
                    if not town:
                        continue
                    #`ex. 西町４丁目 -> 西町
                    re_result = re_compile.search(town)
                    if re_result:
                        town = re_result.group(1)
                        
                pkeys_str = ret_row["pref"] +"\t"+ ret_row["city"]
                if "town" in pkeys:
                    pkeys_str += ( "\t" + town )

                ret_datas_tmp = self.calc_summary_sub(pkeys_str,
                                                      ret_datas_tmp,
                                                      year_quaters,
                                                      ret_row )
        return ret_datas_tmp
    

    def calc_summary_sub( self, pkeys_str,ret_datas_tmp,year_quaters,ret_row ):
        
        if not pkeys_str in ret_datas_tmp:
            ret_datas_tmp[pkeys_str] = {}
            
            for y_quarter in year_quaters:
                ret_datas_tmp[pkeys_str][y_quarter] = {}
                
                for build_type in ["newbuild","sumstock"]:
                    count_key = build_type +"_sold_count"
                    price_key = build_type +"_sold_price"
                    ret_datas_tmp[pkeys_str][y_quarter][count_key] = 0
                    ret_datas_tmp[pkeys_str][y_quarter][price_key] = 0
                
        year_quatar = ret_row["trade_year_q"]
        build_type  = self.newbuild_or_sumstock( ret_row )
        count_key = build_type +"_sold_count"
        price_key = build_type +"_sold_price"
        
        ret_datas_tmp[pkeys_str][year_quatar][count_key] += 1
        ret_datas_tmp[pkeys_str][year_quatar][price_key] += ret_row["price"]

        # 価格帯別集計
        price_m = self.round_200m( ret_row["price"] )
        price_m_key = "%s_sold_price_m_%s_count" % (build_type, price_m)
        if not price_m_key in ret_datas_tmp[pkeys_str][year_quatar]:
            ret_datas_tmp[pkeys_str][year_quatar][price_m_key] = 0
        ret_datas_tmp[pkeys_str][year_quatar][price_m_key] += 1
        
        return ret_datas_tmp
    

    # 200万円単位で丸め
    def round_200m(self, price):
        price_m = round( price /2000000 ) * 2
        return price_m
    
    
    def conv_summary_to_list(self, ret_datas_tmp ):
    
        ret_datas = []
        for pref_city, ret_datas_tmp_2 in ret_datas_tmp.items():
            pkeys = pref_city.split("\t")
            summaries = []
            for trade_year_q in reversed( sorted( ret_datas_tmp_2.keys() )) :
                summary = ret_datas_tmp_2[trade_year_q]
                summary["sold_trade_year_q"] = trade_year_q

                for summary_key in summary.keys():

                    if summary_key in ["newbuild_sold_count",
                                       "sumstock_sold_count" ]:
                        if not summary[summary_key]:
                            continue
                        count_key = summary_key
                        price_key = summary_key.replace("_count","_price")
                        
                        #平均価格
                        summary[price_key] = \
                            round(summary[price_key] / summary[count_key]);
                        # 週次の値にする為、計12で除算
                        summary[count_key] = round(summary[count_key] / 1.2 ) /10;
                    elif "_sold_price_m_" in summary_key:
                        count_key = summary_key
                        # 週次の値にする為、計12で除算
                        summary[count_key] = round(summary[count_key] / 1.2 ) /10;

                summaries.append(summary)

            summary_json = json.dumps(summaries,      ensure_ascii=False)
                
            if len(pkeys) == 2:
                ret_datas.append(
                    {"pref":pkeys[0],
                     "city":pkeys[1],
                     "summary" :json.dumps(summaries,  ensure_ascii=False) })
            elif len(pkeys) == 3:
                ret_datas.append(
                    {"pref":pkeys[0],
                     "city":pkeys[1],
                     "town":pkeys[2],
                     "summary" :json.dumps(summaries,  ensure_ascii=False) })
                    
        return ret_datas


    def newbuild_or_sumstock( self, ret_row ):
        if not ret_row["build_year"]:
            return "sumstock"
        
        year_diff = int(ret_row["trade_year_q"]/10) - int(ret_row["build_year"])
        if year_diff <= 2:
            return "newbuild"
        return "sumstock"
        
