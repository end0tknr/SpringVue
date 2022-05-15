#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.adatascientist         import DataScientistService
from service.mlit_fudousantorihiki  import MlitFudousanTorihikiService
from service.kokusei_population_b01 import KokuseiPopulationB01Service

def main():
    # ds = DataScientistService()
    # ds.calc_correlation_1()
    
    calc_kokusei_pop_b01()
    # calc_mlit_fudousantorihiki()
    

def calc_mlit_fudousantorihiki():
    fudousan_torihiki_service = MlitFudousanTorihikiService()

    ret_vals = fudousan_torihiki_service.get_trend_group_by_city(2020)

    atri_keys  = [
        "pref","city","count","count_pre","price","price_pre"]
    
    for ret_val in ret_vals:
        disp_cols = []
        for atri_key in atri_keys:
            disp_cols.append( str( ret_val[atri_key] ) )
            
        print( "\t".join( disp_cols ) )

def calc_kokusei_pop_b01():
    kokusei_pop_b01_service = KokuseiPopulationB01Service()
    ret_vals = kokusei_pop_b01_service.get_group_by_city()

    atri_keys  = [
        "pref","city","pop","pop_2015","pop_density","setai","setai_2015"]
    
    for ret_val in ret_vals:
        disp_cols = []
        for atri_key in atri_keys:
            disp_cols.append( str( ret_val[atri_key]) )
            
        print( "\t".join( disp_cols ) )

    
if __name__ == '__main__':
    main()
