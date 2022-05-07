#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.kokusei_population_b01 import KokuseiPopulationB01Service
from service.kokusei_population_b02 import KokuseiPopulationB02Service
from service.kokusei_population_b06 import KokuseiPopulationB06Service
from service.kokusei_population_b12 import KokuseiPopulationB12Service
from service.kokusei_population_b18 import KokuseiPopulationB18Service

def main():


    service_classes = [
        # KokuseiPopulationB01Service(),
        # KokuseiPopulationB02Service(),
        # KokuseiPopulationB06Service(),
        # KokuseiPopulationB12Service(),
        KokuseiPopulationB18Service(),
    ]

    for service_class in service_classes:
        src_datas = service_class.download_src_data()
        service_class.save_tbl_rows(src_datas)

if __name__ == '__main__':
    main()

