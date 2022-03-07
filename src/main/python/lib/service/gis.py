#!python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from jeraconv import jeraconv
import appbase
import csv
import glob
import os
import re
import shutil
import subprocess
import tempfile
import urllib.request

src_base_url = "https://nlftp.mlit.go.jp/ksj/gml/data/"

src_path = {
    # https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v3_0.html
    "gyosei_kuiki" : "N03/N03-2021/N03-20210101_GML.zip",
    #https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-L01-v3_0.html
    "chika_koji"   : "L01/L01-21/L01-21_GML.zip",
    #https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-L02-v3_0.html
    "pref_chika"   : "L02/L02-21/L02-21_GML.zip",
    
    # ▲TODO 要scraping
    # https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-A29-v2_1.html
    # https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-L03-a.html
    # https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-L03-b.html

}


src_zip = "tmp_master.zip"
master_csv = "KEN_ALL.CSV"
logger = appbase.AppBase.get_logger()


class GisService(appbase.AppBase):

    def __init__(self):
        pass

    # https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-A29-v2_1.html
    # のように、全国のdataを1つのzipで提供されていない場合がある為、scraping
    def scrape_download_urls(self, datalist_url):
        html_content = urllib.request.urlopen(datalist_url).read()
        soup = BeautifulSoup(html_content, 'html.parser')

        regexp = re.compile('(^.+/)[^/]*$')
        reg_result = regexp.search(datalist_url)
        base_data_url = reg_result.group(1)
        
        datalist_trs = \
            soup.select("table.mb30.responsive-table > tbody > tr")

        j2w = jeraconv.J2W() # 和暦→西暦変換
        regexp = re.compile('([^\'\"]+data[^\'\"]+zip)')

        ret_urls = []

        for datalist_tr in datalist_trs:
            url_info = {}
            tds = datalist_tr.select("td")
            if len(tds) == 0:
                continue
            
            url_info["id"]   = tds[0].text.strip()
            url_info["year"] = j2w.convert( tds[2].text.strip() )

            a_onclick = tds[5].select("a")[0]["onclick"]
            reg_result = regexp.search(a_onclick)
            if not reg_result:
                print("ERROR fail regexp",a_onclick)
                continue

            url_info["url"] = base_data_url + reg_result.group(1)
            ret_urls.append(url_info)
            
        return ret_urls

    def set_db_client_encoding(self,encoding):
        db_conn = self.db_connect()
        cursor = db_conn.cursor()
        sql = "set client_encoding to %s" % (encoding)
        cursor.execute(sql)
        db_conn.commit()
        return True
    
    def reset_db_client_encoding(self):
        db_conn = self.db_connect()
        cursor = db_conn.cursor()
        sql = "reset client_encoding"
        cursor.execute(sql)
        db_conn.commit()
        return True
    
    def drop_master_tbl(self, tbl_name ):
        db_conn = self.db_connect()
        cursor = db_conn.cursor()
        sql = "DROP TABLE IF EXISTS %s" % (tbl_name)
        cursor.execute(sql)
        db_conn.commit()
        return True
    
    def create_master_tbl(self, sql ):
        db_conn = self.db_connect()
        cursor = db_conn.cursor()
        cursor.execute(sql)
        db_conn.commit()
        return True
        
    def insert_master_tbl(self, sql ):
        db_conn = self.db_connect()
        cursor = db_conn.cursor()
        cursor.execute(sql)
        db_conn.commit()
        return True

        
    def get_download_url(self, data_name):
        master_src_url = src_base_url + src_path[data_name]
        return master_src_url

    def download_master(self, master_src_url, data_name ):

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_zip_path = os.path.join(tmp_dir, src_zip)
            try:
                data = urllib.request.urlopen(master_src_url).read()
                
                with open(tmp_zip_path, mode="wb") as fh:
                    fh.write(data)

                shutil.unpack_archive(tmp_zip_path, tmp_dir)
                shape_paths = glob.glob(tmp_dir+'/**/*.shp', recursive=True)
            
                ret_sqls = []
                for shape_path in shape_paths :
                    ret_sql = {}
                    ret_sql["create"] = \
                        self.shape_to_create_pgsql(shape_path,data_name)
                    ret_sql["insert"] = \
                        self.shape_to_insert_pgsql(shape_path,data_name)
                    ret_sqls.append(ret_sql)

                return ret_sqls
            except Exception as e:
                print(e)
                print("fail",master_src_url)

        return None
                
    def shape_to_create_pgsql(self,shape_path,data_name):
        
        conf = self.get_conf()
        shape_cmd = \
            [conf["gis"]["shp2pgsql_cmd"],"-p",shape_path,data_name]
        shape_cmd_str = " ".join( shape_cmd )
        logger.info( shape_cmd_str )

        try:
            result = subprocess.run(shape_cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding="utf8",
                                    text=True)

        except Exception as e:
            print("ERROR", e)
            return None
        
        if result.returncode != 0:
            logger.error(result.stdout +"\n"+ result.stderr)
            return None

        return result.stdout
            
                
    def shape_to_insert_pgsql(self,shape_path,data_name):
        
        conf = self.get_conf()
        shape_cmd = \
            [conf["gis"]["shp2pgsql_cmd"],"-W","cp932","-a",shape_path,data_name]
        shape_cmd_str = " ".join( shape_cmd )
        logger.info( shape_cmd_str )

        try:
            result = subprocess.run(shape_cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding="utf8",
                                    text=True)

        except Exception as e:
            print("ERROR", e)
            return None
        
        if result.returncode != 0:
            logger.error(result.stdout +"\n"+ result.stderr)
            return None

        return result.stdout
