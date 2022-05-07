#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.kokusei2015_population_003 import Kokusei2015Population003Service

def main():

    service_classes = [
        Kokusei2015Population003Service(),
    ]

    for service_class in service_classes:
        src_datas = service_class.download_src_data()
        service_class.save_tbl_rows(src_datas)

if __name__ == '__main__':
    main()

