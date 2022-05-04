#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.estat_jutakutochi_d001 import EstatJutakuTochiD001Service
from service.estat_jutakutochi_d002 import EstatJutakuTochiD002Service
from service.estat_jutakutochi_e006 import EstatJutakuTochiE006Service
from service.estat_jutakutochi_e030 import EstatJutakuTochiE030Service
from service.estat_jutakutochi_e033 import EstatJutakuTochiE033Service
from service.estat_jutakutochi_e044 import EstatJutakuTochiE044Service
from service.estat_jutakutochi_e048 import EstatJutakuTochiE048Service
from service.estat_jutakutochi_e049 import EstatJutakuTochiE049Service

def main():

    service_classes = [
        # EstatJutakuTochiD001Service(),
        # EstatJutakuTochiD002Service(),
        # EstatJutakuTochiE006Service(),
        # EstatJutakuTochiE030Service(),
        # EstatJutakuTochiE033Service(),
        # EstatJutakuTochiE044Service(),
        # EstatJutakuTochiE048Service(),
        EstatJutakuTochiE049Service(),
    ]

    for service_class in service_classes:
        src_datas = service_class.download_src_data()
        service_class.save_tbl_rows(src_datas)

if __name__ == '__main__':
    main()
