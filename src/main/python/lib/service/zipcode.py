#!python
# -*- coding: utf-8 -*-

import csv
import glob
import os
import shutil
import tempfile
import urllib.request

# https://www.post.japanpost.jp/zipcode/dl/readme.html
master_src_url = \
    "https://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip"
master_csv_zip = "ken_all.zip"
master_csv = "KEN_ALL.CSV"
logger = None

master_heads = [
    "全国地方公共団体コード","旧郵便番号","郵便番号",
    "都道府県ｶﾅ","市区町村ｶﾅ","町域ｶﾅ",
    "都道府県",  "市区町村",  "町域" ]

class ZipcodeService():
    
    def __init__(self):
        global logger
        logger = self.get_logger()

    def download_master(self):
        ret_data = []
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_zip_path =os.path.join(tmp_dir, master_csv_zip)
            tmp_csv_path =os.path.join(tmp_dir, master_csv)
        
            try:
                data = urllib.request.urlopen(master_src_url).read()

                with open(tmp_zip_path, mode="wb") as fh:
                    fh.write(data)

                shutil.unpack_archive(tmp_zip_path, tmp_dir)

                with open(tmp_csv_path) as fh:
                    csvreader = csv.reader(fh)
                    for master_body in csvreader:
                        i = 0
                        master_row = {}
                        for head_col in master_heads:
                            master_row[head_col] = master_body[i]
                            i += 1
                            
                        ret_data.append(master_row)
            except:
                print("fail",master_src_url)

            return ret_data
    
