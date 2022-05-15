#!python
# -*- coding: utf-8 -*-

from jeraconv import jeraconv
from psycopg2  import extras # for bulk insert

import appbase
import copy
import csv
import glob
import json
import os
import re
import tempfile
import urllib.request
import zipfile
from service.city       import CityService

# refer urls are below.
#   https://www.land.mlit.go.jp/webland/download.html

# 事前にブラウザでダウンロードを実行することで
# 初めてダウンロード用 zipが作成されます
target_host  = 'https://www.land.mlit.go.jp'
target_path  = '/webland/zip/All_20111_20214.zip'
#target_path  = '/webland/zip/All_20212_20213.zip'

row_filters = {"種類" : ["宅地(土地と建物)","宅地(土地)","中古マンション等"],
               "地域" : ["住宅地","宅地見込地"] }
col_filters = {"種類"            :"shurui",
               "地域"            :"chiiki",
               "都道府県名"      :"pref",
               "市区町村名"      :"city",
               "地区名"          :"street",
               "取引価格（総額）":"price",
               "面積（㎡）"      :"area_m2",
               "建築年"          :"build_year",
               "取引時点"        :"trade_year" }
bulk_insert_size = 20
logger = None

class MlitFudousanTorihikiService(appbase.AppBase):

    def __init__(self):
        global logger
        logger = self.get_logger()

    def save_tbl_rows(self, rows):
        logger.info("start")
        logger.info(rows[0])
        row_groups = self.divide_rows(rows, bulk_insert_size)

        sql = """
INSERT INTO mlit_fudousantorihiki
(shurui,chiiki,pref,city,street,price,area_m2,build_year,trade_year)
VALUES %s
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
    
    def divide_rows(self, org_rows, chunk_size):
        i = 0
        chunk = []
        ret_rows = []
        for org_row in org_rows:
            chunk.append( ( org_row['shurui'],
                            org_row['chiiki'],
                            org_row['pref'],
                            org_row['city'],
                            org_row['street'],
                            org_row['price']      or None,
                            org_row['area_m2']    or None,
                            org_row['build_year'] or None,
                            org_row['trade_year'] or None) )
            
            if len(chunk) >= chunk_size:
                ret_rows.append(chunk)
                chunk = []
            i += 1

        if len(chunk) > 0:
            ret_rows.append(chunk)

        return ret_rows

    def __filter_data(self,org_row):

        for atri_key in row_filters:
            if not atri_key in org_row:
                return None
            if not org_row[atri_key] in row_filters[atri_key]:
                return None

        ret_row = {}
        for org_key,new_key in col_filters.items():
            ret_row[new_key] = org_row[org_key]

        # 例 2000㎡以上->2000, 2014年第４四半期->2014
        re_compile = re.compile("^(\d+)")
        for atri_key in ["area_m2", "trade_year"]:
            if not ret_row[atri_key]:
                continue
            re_result = re_compile.search(ret_row[atri_key])
            if re_result:
                ret_row[atri_key] = re_result.group(1)
                
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

        return ret_row
            

    def download_master(self):
        download_url = target_host + target_path
        logger.info(download_url)
        
        ret_data = []
    
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_zip_path =os.path.join(tmp_dir, "tmp.zip")

            try:
                data = urllib.request.urlopen(download_url).read()
                with open(tmp_zip_path, mode="wb") as fh:
                    fh.write(data)

                zip = zipfile.ZipFile(tmp_zip_path, "r")
                zip.extractall(path=tmp_dir)
                zip.close()

            except Exception as e:
                logger.error("fail", download_url)
                logger.error(e)
                return []

            for csv_path in glob.glob(tmp_dir + '/*.csv' ):
                logger.info(csv_path)
                csv_name = str( os.path.split(csv_path)[1] )

                with open(csv_path, encoding='cp932', newline="") as f:
                    # key-value形式での読込み
                    dict_reader = csv.DictReader(f, delimiter=",", quotechar='"')
                    new_rows = []
                    i = 0
                    for dict_row in dict_reader:
                        i += 1
                        if i % 10000 == 0:
                            logger.info( csv_path +" "+str(i) )
                            
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
        
    def get_trend_group_by_city(self,trade_year):

        pre_year = trade_year - 5 
        pre_vals_tmp = self.get_group_by_city(pre_year  )

        pre_vals = {}
        for pre_val_tmp in pre_vals_tmp:
            pref_city = "\t".join([pre_val_tmp["pref"],pre_val_tmp["city"] ] )
            del pre_val_tmp["pref"]
            del pre_val_tmp["city"]
            pre_vals[pref_city] = pre_val_tmp

        ret_vals =     self.get_group_by_city(trade_year)
        for ret_val in ret_vals:
            pref_city = "\t".join([ret_val["pref"],ret_val["city"] ] )
            if not pref_city in pre_vals:
                logger.error("not found " + pref_city)
                
                ret_val["count_pre"] = 0
                ret_val["price_pre"] = 0
                continue

            ret_val["count_pre"] = pre_vals[pref_city]["count"]
            ret_val["price_pre"] = pre_vals[pref_city]["price"]

            
        return ret_vals
        
    def get_group_by_city(self,trade_year):
        sql = """
select
  pref, city, trade_year, count(*) as count,
  avg(price)::numeric::bigint as price
from mlit_fudousantorihiki
where shurui in ('宅地(土地と建物)','中古マンション等') and
      trade_year=%s
group by pref,city,trade_year
"""
        ret_data = []
        
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:
                try:
                    db_cur.execute(sql % (trade_year))
                    for ret_row in  db_cur.fetchall():
                        ret_data.append( dict( ret_row ))
                    
                except Exception as e:
                    logger.error(e)
                    logger.error(sql)
                    return []
        return ret_data
