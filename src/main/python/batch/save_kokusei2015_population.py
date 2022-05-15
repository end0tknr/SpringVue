#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.kokusei2015_population_003 import Kokusei2015Population003Service
from service.kokusei2015_population_007 import Kokusei2015Population007Service
from service.kokusei2015_population_013 import Kokusei2015Population013Service
from service.kokusei2015_population_018 import Kokusei2015Population018Service

def main():

    service_classes = [
        # Kokusei2015Population003Service(),
        # Kokusei2015Population007Service(),
        # Kokusei2015Population013Service(),
        Kokusei2015Population018Service(),
    ]

    for service_class in service_classes:
        service_class.del_tbl_rows()
        
        src_datas = service_class.download_src_data()
        
        service_class.save_tbl_rows(src_datas)

if __name__ == '__main__':
    main()

