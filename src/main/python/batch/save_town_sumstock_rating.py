#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.town_sumstock_rating import TownSumStockRatingService

def main():
    town_rating_service = TownSumStockRatingService()
    town_rating_service.calc_save_ratings()

if __name__ == '__main__':
    main()


