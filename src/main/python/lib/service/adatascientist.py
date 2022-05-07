#!python
# -*- coding: utf-8 -*-
import appbase
from service.population_city       import PopulationCityService
from service.mlit_fudousantorihiki import MlitFudousanTorihikiService
class DataScientistService(appbase.AppBase):

    def __init__(self):
        pass

    def calc_correlation_1(self):
        fudousan_torihiki = MlitFudousanTorihikiService()
        group_by_city = fudousan_torihiki.get_group_by_city(2020)
        print( group_by_city )
        
