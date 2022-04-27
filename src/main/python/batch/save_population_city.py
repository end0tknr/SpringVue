#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.population_city import PopulationCityService

def main():
    population_city_service = PopulationCityService()
    excel_infos = population_city_service.download_master()
    print( excel_infos )
    
    # for csv_info in csv_infos:
    #     fudosan_tochi_service.save_tbl_rows( csv_info[1] )

if __name__ == '__main__':
    main()

