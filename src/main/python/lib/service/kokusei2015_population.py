#!python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from psycopg2  import extras # for bulk insert

import appbase
import os
import re
import urllib.request

logger = appbase.AppBase().get_logger()

download_host = "https://www.e-stat.go.jp"
download_base_url = \
    download_host + "/stat-search/files?toukei=00200521&tstat=000001080615"

class Kokusei2015PopulationService(appbase.AppBase):

    def calc_download_filename(self,headers, download_url):

        re_compile_1 = "^attachment;\s+"
        filename = None
        for header in headers:
            if header[0] == "Content-Disposition":
                filename = self.calc_download_filename_sub(header[1])
                break

        if filename:
            return filename
        
        filename = os.basename(download_url)
        if filename:
            return filename
        
        return None
                
        
    def find_urls_for_pref(self):
        try:
            res = urllib.request.urlopen( download_base_url )
        except Exception as e:
            logger.error(download_base_url)
            logger.error(e)
            return []

        soup = BeautifulSoup( res.read(), 'html.parser')
        pref_hrefs = soup.select(".stat-matter3 a")

        re_compile = re.compile("\d\d([^\d]+).+\[65件\]")

        ret_urls = []
        for pref_href in pref_hrefs:
            re_result = re_compile.search( pref_href.text.strip() )
            if not re_result:
                continue

            pref_name = re_result.group(1).strip()
            pref_url = download_host + pref_href["href"]
            ret_urls.append( [pref_name , pref_url] )
        return ret_urls
    
        
    def download_src_data(self):
        pref_urls = self.find_urls_for_pref()

        ret_data = []
        for pref_url in pref_urls:
            download_url = self.find_download_url(pref_url[1],
                                                  self.get_data_src_tbl_no())
            logger.info( pref_url[0] +" "+download_url )
            
            downloaded = self.download_file( download_url )
            tmp_ret_data = self.load_csv_content( downloaded["content"] )
            ret_data.extend( tmp_ret_data )
            
        return ret_data


    def find_download_url(self, pref_url, tbl_no):
        logger.info( pref_url +" "+ tbl_no )

        try:
            res = urllib.request.urlopen( pref_url )
        except Exception as e:
            logger.error(pref_url)
            logger.error(e)
            return None
        
        soup = BeautifulSoup( res.read(), 'html.parser')
        tbl_uls = soup.select(".stat-dataset_list-detail")

        for tbl_ul in tbl_uls:
            li_elms = tbl_ul.select("li")
            tmp_tbl_no = li_elms[0].text.strip().split()
            if tmp_tbl_no[1]  != tbl_no:
                continue
            
            a_elms = tbl_ul.select("a")
            download_path = a_elms[1]["href"]
            return download_host + download_path

        return None
    
            
    def download_file(self, download_url):
        logger.info(download_url)
        try:
            res = urllib.request.urlopen(download_url)
        except Exception as e:
            logger.error(download_url)
            logger.error(e)
            return None

        content = res.read()
        filename = self.calc_download_filename(res.getheaders(),
                                               download_url )
        return {"filename":filename, "content":content}


    def calc_download_filename(self,headers, download_url):

        re_compile_1 = "^attachment;\s+"
        filename = None
        for header in headers:
            if header[0] == "Content-Disposition":
                filename = self.calc_download_filename_sub(header[1])
                break

        if filename:
            return filename
        
        filename = os.basename(download_url)
        if filename:
            return filename
        
        return None
    
                
    def calc_download_filename_sub(self,header_vals_str):
        header_vals = re.compile("\s*;\s*").split(header_vals_str)

        # RFC-6266
        re_compile = re.compile("^filename\*\s*=(.+)''(.+)")
        for header_val in header_vals:
            re_result = re_compile.search( header_val )
            if not re_result:
                continue

            filename_enc = re_result.group(1)
            filename     = re_result.group(2)
            filename = filename.encode(filename_enc).decode("UTF-8")
            return filename
        
        re_compile = re.compile("^filename\s*=['\"]?(.+)['\"]?")
        for header_val in header_vals:
            re_result = re_compile.search( header_val )
            if not re_result:
                continue

            filename     = re_result.group(1)
            return filename
        
        return None
            
    # for bulk insert
    def divide_rows(self, org_rows, chunk_size, atri_keys):
        i = 0
        chunk = []
        ret_rows = []
        for org_row in org_rows:
            new_tuple = ()
            for atri_key in atri_keys:
                new_tuple += (org_row[atri_key],)
            chunk.append( new_tuple )
            
            if len(chunk) >= chunk_size:
                ret_rows.append(chunk)
                chunk = []
            i += 1

        if len(chunk) > 0:
            ret_rows.append(chunk)

        return ret_rows


    def save_tbl_rows(self, rows):
        logger.info("start")
        logger.info(rows[0])

        bulk_insert_size = self.get_conf()["common"]["bulk_insert_size"]
        atri_keys = self.get_insert_cols()
        row_groups = self.divide_rows(rows, bulk_insert_size, atri_keys )
        
        sql = self.get_insert_sql()
        sql = sql % (",".join(atri_keys), "%s")
        
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
