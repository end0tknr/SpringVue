#!python3
# -*- coding: utf-8 -*-

import getopt
import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )

from service.city_rating import CityRatingService

def main():
    city_rating_service = CityRatingService()
    
    city_rating_service.calc_save_ratings()
    

if __name__ == '__main__':
    main()
