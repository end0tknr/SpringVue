#!python
# -*- coding: utf-8 -*-

from service.sumstock             import SumStockService
from service.town_newbuild_rating import TownNewBuildRatingService
import appbase

logger = appbase.AppBase().get_logger()
calc_type = "sumstock"

class TownSumStockRatingService(TownNewBuildRatingService):

    def __init__(self):
        self.calc_type   = calc_type
        self.rating_type = calc_type + "_rating"
        self.sales_result_class = SumStockService()
