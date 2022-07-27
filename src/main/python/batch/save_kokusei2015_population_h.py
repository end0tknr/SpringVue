#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.kokusei2015_population_h03 import Kokusei2015PopulationH03Service
from service.kokusei2015_population_h06 import Kokusei2015PopulationH06Service
from service.kokusei2015_population_h07 import Kokusei2015PopulationH07Service
from service.kokusei2015_population_h08 import Kokusei2015PopulationH08Service

def main():

    service_classes = [
        Kokusei2015PopulationH03Service(),
        Kokusei2015PopulationH06Service(),
        Kokusei2015PopulationH07Service(),
        Kokusei2015PopulationH08Service(),
    ]
    
    for service_class in service_classes:
        download_urls = service_class.get_download_urls()
        for download_url in download_urls:
            pref     = download_url[0]
            pref_url = download_url[1]
            service_class.download_save_data_src(pref_url)
        
if __name__ == '__main__':
    main()
