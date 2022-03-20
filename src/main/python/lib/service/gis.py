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
import sys
import tempfile
import urllib.request

# soup.select() において、以下errorとなることがある為
# RecursionError: maximum recursion depth exceeded
sys.setrecursionlimit(5000)

default_select_cond = {"id":"全国"}
default_geodetic    = '世界測地系'

src_host = "https://nlftp.mlit.go.jp"
src_path = {
    "gis_gyosei_kuiki" :
    {"index_page": "/ksj/gml/datalist/KsjTmplt-N03-v3_0.html",
     "select_cond": default_select_cond},
    "gis_chika_koji" :
    {"index_page": "/ksj/gml/datalist/KsjTmplt-L01-v3_0.html",
     "select_cond": default_select_cond},
    "gis_chika" :
    {"index_page" : "/ksj/gml/datalist/KsjTmplt-L02-v3_0.html",
     "select_cond": default_select_cond},
    "gis_youto_chiiki" :
    {"index_page": "/ksj/gml/datalist/KsjTmplt-A29-v2_1.html",
     "select_cond": {}},
    "gis_tochi_riyo" :
    {"index_page": "/ksj/gml/datalist/KsjTmplt-L03-a.html",
     "select_cond": {}},
    "gis_tochi_riyo_saibun" :
    {"index_page": "/ksj/gml/datalist/KsjTmplt-L03-b.html",
     "select_cond": {}},
    "gis_tochi_riyo_shousai" :
    {"index_page": "/ksj/gml/datalist/KsjTmplt-L03-b-c.html",
     "select_cond": {}},
    "gis_jinko_shuchu" :
    {"index_page": "/ksj/gml/datalist/KsjTmplt-A16-v2_3.html",
     "select_cond": {}},
    "gis_jinko_suikei_1km" :
    {"index_page": "/ksj/gml/datalist/KsjTmplt-mesh1000h30.html",
     "select_cond": {}},
    "gis_jinko_suikei_500m" :
    {"index_page": "/ksj/gml/datalist/KsjTmplt-mesh500h30.html",
     "select_cond": {}},
}

logger = appbase.AppBase.get_logger()

class GisService(appbase.AppBase):
    def __init__(self):
        pass

    def get_data_names(self):
        return sorted(list( src_path.keys() ))
        
    def get_index_page_url(self, data_name):
        return src_host + src_path[data_name]["index_page"]
    
    def get_select_data_cond(self, data_name):
        if not "select_cond" in src_path[data_name]:
            return {}
        return src_path[data_name]["select_cond"]
    
    def chk_col_name_and_comment(self,col_name,col_name_tmp,comment):
        if col_name==col_name_tmp:
            return comment

        # 以降は「20XX年合算先メッシュ（GASSAN_20XX）」のような場合の対応
        # 例 https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-mesh1000h30.html
        
        # 西暦の下2桁を抽出
        re_result = re.compile("20(\d\d)").search(col_name)
        if not re_result:
            return None
        
        yy = re_result.group(1)

        re_compile = re.compile("20(XX)",re.IGNORECASE)
        col_name_tmp = re.sub(re_compile,"20"+yy,col_name_tmp)

        if col_name==col_name_tmp:
            comment = re.sub(re_compile,"20"+yy,comment)
            return comment

        return None


    # テーブル名称?を scrape
    def find_db_tbl_comment(self,index_page_url):
        html_content = urllib.request.urlopen(index_page_url).read()
        soup = BeautifulSoup(html_content, 'html.parser')
        ahrefs = soup.select("div.breadcrumb-list a")

        re_result = re.compile("^([^（\(]+)").search(
            ahrefs[-1].text.strip() )

        if re_result:
            return re_result.group(1)
        return None
        

    # nlftp.mlit.go.jp からの shape ファイルは変換し、db登録されますが
    # table column名 が 例:n03_001 で分かりづらい為、
    # htmlをscrapeし、分かりやすいコメントを探します。
    def find_db_col_comment(self,index_page_url):

        html_content = urllib.request.urlopen(index_page_url).read()
        soup = BeautifulSoup(html_content, 'html.parser')

        trs = soup.select("table.tablelist.responsive-table > tbody > tr")
        is_found_col_area = None
        ret_data = {}

        # column名とコメントの抽出用 正規表現
        re_compile = re.compile(
            '([^\(\)（）]+)\s*[（\(]([^\(\)（）]+)[\)）]', flags=(re.DOTALL) )

        for tr in trs:
            if not is_found_col_area:
                ths = tr.select("th")
                if len(ths) == 4 and \
                   re.compile('属性名'  ).search(ths[1].text) and \
                   re.compile('説明'    ).search(ths[2].text) and \
                   re.compile('属性の型').search(ths[3].text):
                   is_found_col_area = True
                   continue
            else:
                tds = tr.select("td")
                if len(tds) != 3:
                    continue

                re_result = re_compile.search(tds[0].text)
                if re_result and len( re_result.group(1).strip() ):
                    ret_data[re_result.group(2).lower()] = \
                        re_result.group(1).strip()

        return ret_data

        
    # https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-A29-v2_1.html
    # のように、全国のdataを1つのzipで提供されていない場合がある為、scraping
    def find_data_urls(self,index_page_url):
        logger.info("start " + index_page_url)
        
        html_content = urllib.request.urlopen(index_page_url).read()
        soup = BeautifulSoup(html_content, 'html.parser')

        reg_result = re.compile('(^.+/)[^/]*$').search(index_page_url)
        data_url_base = reg_result.group(1)

        j2w = jeraconv.J2W() # 和暦→西暦変換
        
        # 行政区域のpageは、<tr><tr> のように htmlが誤っており
        # BeautifulSoup が発狂するので、ここだけ、正規表現を使用
        tmp_css_selector = "table.mb30.responsive-table > tbody"
        try:
            tbody = soup.select(tmp_css_selector)[0]
            tbody = str(tbody)
            trs = re.compile("(<tr>.+?</tr>)",flags=(re.DOTALL)).findall(tbody)
        except Exception as e:
            logger.error("soup.select(%s)" % (tmp_css_selector) )
            logger.error(e)

        zip_path_regexp = re.compile('([^\'\"]+data[^\'\"]+zip)')
        ret_urls = []
        
        for tr in trs:
            tds = BeautifulSoup(tr, 'html.parser').select("td")
            
            if len(tds) == 0:
                continue
            
            url_info = {}
            url_info["id"]      = tds[0].text.strip()
            url_info["geodetic"]= tds[1].text.strip()
            url_info["year"]    = j2w.convert( tds[2].text.strip() )
            a_onclick = tds[5].select("a")[0]["onclick"]
            reg_result = zip_path_regexp.search(a_onclick)
            if not reg_result:
                print("ERROR fail regexp",a_onclick)
                continue

            data_path = reg_result.group(1)
            if re.compile('^/' ).search(data_path):
                url_info["url"] = src_host + data_path
            else:
                url_info["url"] = data_url_base + data_path

            if url_info["geodetic"] == default_geodetic:
                ret_urls.append(url_info)
            
        return ret_urls

    # def set_db_client_encoding(self,encoding):
    #     db_conn = self.db_connect()
    #     cursor = db_conn.cursor()
    #     sql = "set client_encoding to %s" % (encoding)
    #     cursor.execute(sql)
    #     db_conn.commit()
    #     return True
    
    # def reset_db_client_encoding(self):
    #     db_conn = self.db_connect()
    #     cursor = db_conn.cursor()
    #     sql = "reset client_encoding"
    #     cursor.execute(sql)
    #     db_conn.commit()
    #     return True
    
    # def drop_master_tbl(self, tbl_name ):
    #     db_conn = self.db_connect()
    #     cursor = db_conn.cursor()
    #     sql = "DROP TABLE IF EXISTS %s" % (tbl_name)
    #     cursor.execute(sql)
    #     db_conn.commit()
    #     return True
    
    def create_master_tbl(self, sql ):
        logger.info("start " + sql)
        try:
            db_conn = self.db_connect()
            cursor = db_conn.cursor()
            cursor.execute(sql)
            # 引数で受領する sql文内にcommitがある為、commit 不要
            #db_conn.commit()
        except Exception as e:
            logger.error(e)
            logger.error(sql)
            return False
        return True
        
    def insert_master_tbl(self, sql ):

        if len(sql) > 200:
            logger.info("start " + sql[:200])
        else:
            logger.info("start " + sql)

        try:
            db_conn = self.db_connect()
            cursor = db_conn.cursor()
            cursor.execute(sql)
            db_conn.commit()
        except Exception as e:
            logger.error(e)
            logger.error(sql)
            return False
        return True

    def chk_select_cond(self, select_cond, data_url ):
        for cond_key,cond_val in select_cond.items():
            
            if not cond_key in data_url.keys():
                return False
            
            if data_url[cond_key] != cond_val:
                return False
            
        return True

    def download_master(self, master_src_url, data_name ):
        logger.info("start " + master_src_url)

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_zip_path = os.path.join(tmp_dir, "tmp_master.zip")
            
            try:
                data = urllib.request.urlopen(master_src_url).read()
                with open(tmp_zip_path, mode="wb") as fh:
                    fh.write(data)
            except Exception as e:
                logger.error("urllib.request.urlopen() or open()")
                logger.error(e)
                
            try:
                shutil.unpack_archive(tmp_zip_path, tmp_dir)
            except Exception as e:
                logger.error("shutil.unpack_archive() "+tmp_dir)
                logger.error(e)
                    
            shape_paths = glob.glob(tmp_dir+'/**/*.shp', recursive=True)
                
            ret_sqls = []
            for shape_path in shape_paths :
                logger.debug("shape_path " + shape_path)
                
                ret_sql = {}
                ret_sql["create"] = \
                    self.shape_to_create_pgsql(shape_path,data_name)
                ret_sql["insert"] = \
                    self.shape_to_insert_pgsql(shape_path,data_name)
                ret_sqls.append(ret_sql)
                
            return ret_sqls

        return None
                
    def shape_to_create_pgsql(self,shape_path,data_name):
        conf = self.get_conf()

        # shp2pgsql で以下のerrorとなることがある為「-W cp932」を追加
        # Unable to convert field name to UTF-8
        # (iconv reports "Invalid or incomplete multibyte or wide character").
        # Current encoding is "UTF-8". Try "LATIN1" (Western European), or
        # one of the values described at http://www.gnu.org/software/libiconv/.
        shape_cmd = \
            [conf["common"]["shp2pgsql_cmd"],"-W","cp932","-p",
             shape_path,data_name]
        shape_cmd_str = " ".join( shape_cmd )
        logger.info( shape_cmd_str )

        try:
            result = subprocess.run(shape_cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding="utf8")

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
            [conf["common"]["shp2pgsql_cmd"],"-W","cp932","-a",
             shape_path,data_name]
        shape_cmd_str = " ".join( shape_cmd )
        logger.info( shape_cmd_str )

        try:
            result = subprocess.run(shape_cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding="utf8")

        except Exception as e:
            print("ERROR", e)
            return None
        
        if result.returncode != 0:
            logger.error(result.stdout +"\n"+ result.stderr)
            return None

        return result.stdout
