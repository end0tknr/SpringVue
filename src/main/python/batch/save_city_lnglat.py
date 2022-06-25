#!python3
# -*- coding: utf-8 -*-

import getopt
import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )

from service.city       import CityService

def main():
    city_service = CityService()
    city_service.calc_save_lnglat()

        
if __name__ == '__main__':
    main()
    
