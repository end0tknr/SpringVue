#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.mlit_seisanryokuchi import MlitSeisanRyokuchiService

def main():
    seisan_yrokuchi_service = MlitSeisanRyokuchiService()
    infos = seisan_yrokuchi_service.download_master()
    # print( infos )

    seisan_yrokuchi_service.save_tbl_rows( infos )

if __name__ == '__main__':
    main()
