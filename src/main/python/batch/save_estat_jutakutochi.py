#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.estat_jutakutochi import EstatJutakuTochiService

master_xls = "b013.xls"
target_host = "http://www.e-stat.go.jp"

def main():
    jutaku_tochi_service = EstatJutakuTochiService()
    download_urls = jutaku_tochi_service.find_download_urls()

    for download_url in download_urls:
        parsed_datas = jutaku_tochi_service.download_excel(download_url)
        jutaku_tochi_service.save_tbl_rows(parsed_datas)
    
if __name__ == '__main__':
    main()
    
