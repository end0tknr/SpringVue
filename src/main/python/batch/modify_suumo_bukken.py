#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.city  import CityService
from service.suumo import SuumoService

def main():
    suumo_service = SuumoService()
    city_service  = CityService()

    bukkens = suumo_service.load_all_bukkens()
    for bukken in bukkens:
        address_org = bukken["address"]
        address_new = city_service.parse_pref_city(address_org)

        suumo_service.modify_pref_city(address_org,
                                       address_new[0],
                                       address_new[1],
                                       address_new[2])

if __name__ == '__main__':
    main()


