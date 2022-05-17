#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.soumu_zeisei_j5120b import SoumuZeiseiJ5120bService

def main():
    soumu_service = SoumuZeiseiJ5120bService()

    soumu_service.del_tbl_rows()
        
    src_datas = soumu_service.download_src_data()
    print(src_datas)
        
    soumu_service.save_tbl_rows(src_datas)


if __name__ == '__main__':
    main()


