#!python
# -*- coding: utf-8 -*-

from service.sumstock             import SumStockService
from service.city_newbuild_rating import CityNewBuildRatingService
import appbase

logger = appbase.AppBase().get_logger()
calc_type = "sumstock"

class CitySumStockRatingService(CityNewBuildRatingService):
    
    def __init__(self):
        self.calc_type   = calc_type
        self.rating_type = calc_type + "_rating"
        self.sales_result_class = SumStockService()
