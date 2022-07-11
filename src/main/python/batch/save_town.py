#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.town import TownService

def main():
    town_service = TownService()
    town_service.init_profiles()
    pref_city_towns = town_service.get_all()
    town_service.calc_save_lnglat_by_mlit_gsi( pref_city_towns )


if __name__ == '__main__':
    main()


