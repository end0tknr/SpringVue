#!python
# -*- coding: utf-8 -*-

from bs4          import BeautifulSoup

import appbase
import os
import re
import urllib.request
import xlrd     # for xls
import openpyxl # for xlsx
import tempfile

download_host = 'https://www.e-stat.go.jp'
download_base_url = download_host + \
    "/stat-search/files?page=1&toukei=00200521&tstat=000001136464&tclass1=000001136472"

logger = appbase.AppBase().get_logger()
re_compile_href = re.compile('href="(.*?)"')


class KokuseiPopulationHService(appbase.AppBase):

    

    def conv_hash_to_list(self, ret_datas_tmp):
        ret_datas = []
        for pref_city_town, atri_key_vals in ret_datas_tmp.items():
            (pref,city,town) = pref_city_town.split("\t")
            atri_key_vals["pref"] = pref
            atri_key_vals["city"] = city
            atri_key_vals["town"] = town
            ret_datas.append(atri_key_vals)
        return ret_datas
        
    def get_download_url(self, pref_html,data_name):
        soup     = BeautifulSoup(pref_html, 'html.parser')
        articles = soup.select(".stat-dataset_list-body article")

        for article in articles:
            if not data_name in str(article):
                continue

            a_elms = article.select("a")
            re_result = re_compile_href.search( str(a_elms[1]) )
            if not re_result:
                logger.error("fail parse href for "+a_elms[1] )
                continue

            path = re_result.group(1).replace('&amp;','&')
            return download_host + path

        
    def get_download_urls(self):
        base_html = self.get_http_requests( download_base_url )
        soup = BeautifulSoup(base_html, 'html.parser')

        a_elms = soup.select(".stat-search_result-list a")

        ret_datas = []
        for a_elm in a_elms:
            pref = a_elm.text.strip().split("\n")[0]
            pref = pref.split("：")[1]

            re_result = re_compile_href.search( str(a_elm) )
            if not re_result:
                logger.error("fail parse href for "+a_elm)
                continue
            
            path = re_result.group(1).replace('&amp;','&')
            ret_datas.append( [pref, download_host + path] )
        return ret_datas
