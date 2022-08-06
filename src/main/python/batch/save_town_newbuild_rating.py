#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.town_newbuild_rating import TownNewbuildRatingService

def main():
    town_rating_service = TownNewbuildRatingService()
    town_rating_service.calc_save_ratings()

if __name__ == '__main__':
    main()


