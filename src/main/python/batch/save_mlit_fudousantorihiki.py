#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.mlit_fudousantorihiki import MlitFudousanTorihikiService

def main():
    fudosan_tochi_service = MlitFudousanTorihikiService()
    csv_infos = fudosan_tochi_service.download_master()

    for csv_info in csv_infos:
        fudosan_tochi_service.save_tbl_rows( csv_info[1] )

if __name__ == '__main__':
    main()
