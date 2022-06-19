#!python3
# -*- coding: utf-8 -*-

import getopt
import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )

from service.city             import CityService
from service.gis_gyosei_kuiki import GisGyoseiKuikiService

def main():
    city_service = CityService()
    gyosei_kuiki_service = GisGyoseiKuikiService()

    cities = city_service.get_all_pref_city()
    for city in cities:
        if not city["city"]:
            continue

        if city_service.is_seirei_city(city["city"]) and \
           not "区" in city["city"]:
            continue

        geom_text = gyosei_kuiki_service.calc_bounding_box(city["pref"],
                                                           city["city"])
        near_cities = gyosei_kuiki_service.find_cities_by_bouding_box(geom_text)
        #print(city["city"], near_cities)
        city_service.save_near_cities(city["pref"],city["city"],near_cities)


if __name__ == '__main__':
    main()
    
