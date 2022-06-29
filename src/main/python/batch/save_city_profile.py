#!python3
# -*- coding: utf-8 -*-

import getopt
import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )

from service.city_profile       import CityProfileService

def main():
    city_profile_service = CityProfileService()
    
    city_profile_service.del_profiles()
    # 築年数とは無関係の profile
    profiles = city_profile_service.calc_profiles()
    city_profile_service.save_profiles( profiles )

    # 築年数による profile
    city_profile_service.calc_save_bild_year_profiles()
    

if __name__ == '__main__':
    main()
