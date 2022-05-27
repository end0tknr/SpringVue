#!python3
# -*- coding: utf-8 -*-

import os
import re
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.adatascientist         import DataScientistService
from service.estat_jutakutochi_d002 import EstatJutakuTochiD002Service
from service.estat_jutakutochi_e044 import EstatJutakuTochiE044Service
from service.estat_jutakutochi_e048 import EstatJutakuTochiE048Service
from service.estat_jutakutochi_e049 import EstatJutakuTochiE049Service
from service.estat_jutakutochi_e049 import EstatJutakuTochiE049Service
from service.estat_jutakutochi_e101 import EstatJutakuTochiE101Service
from service.gis_youto_chiiki       import GisYoutoChiikiService
from service.mlit_fudousantorihiki  import MlitFudousanTorihikiService
from service.kokusei_population_b01 import KokuseiPopulationB01Service
from service.kokusei_population_b02 import KokuseiPopulationB02Service
from service.kokusei_population_b12 import KokuseiPopulationB12Service
from service.kokusei_population_b18 import KokuseiPopulationB18Service
from service.suumo                  import SuumoService
from service.soumu_zeisei_j5120b    import SoumuZeiseiJ5120bService


def main():
    # ds = DataScientistService()
    # ds.calc_correlation_1()
    
    # calc_mlit_fudousantorihiki()
    # calc_kokusei_pop_b01()
    # calc_kokusei_pop_b02()
    # calc_kokusei_pop_b12()
    # calc_kokusei_pop_b12_2()
    # calc_kokusei_pop_b18()
    # calc_jutakutochi_d002()
    # calc_jutakutochi_e044()
    # calc_jutakutochi_e048()
    # calc_jutakutochi_e049()
    # calc_jutakutochi_e101()
    # calc_youto_chiiki()
    # calc_suumo_stock_bukken()
    # calc_suumo_sold_bukken()
    calc_soumu_zeisei()

def calc_soumu_zeisei():
    soumu_zeisei = SoumuZeiseiJ5120bService()

    ret_vals = soumu_zeisei.get_vals()
    for ret_val in ret_vals:
        disp_cols = [ret_val["pref"],
                     ret_val["city"],
                     str( ret_val["pop"] ),
                     str( ret_val["salary"] ),
                     str( ret_val["capital_income"] )]
        
        print( "\t".join( disp_cols ) )

def calc_suumo_stock_bukken():
    suumo_service = SuumoService()

    ret_vals = suumo_service.get_stock_vals()
    build_types = ["新築戸建","中古戸建","中古マンション"]
    atri_keys   = ["count","price"]
    for ret_val in ret_vals:
        disp_cols = [ret_val["pref"],ret_val["city"]]
        for build_type in build_types:
            for atri_key in atri_keys:
                key_tmp = "%s_%s" %(build_type,atri_key)
                if key_tmp in ret_val:
                    disp_cols.append( str(ret_val[key_tmp]) )
                else:
                    disp_cols.append("")
        
        print( "\t".join( disp_cols ) )


def calc_suumo_sold_bukken():
    suumo_service = SuumoService()

    ret_vals = suumo_service.get_sold_vals()
    build_types = ["新築戸建","中古戸建","中古マンション"]
    atri_keys   = ["count","price"]
    for ret_val in ret_vals:
        disp_cols = [ret_val["pref"],ret_val["city"]]
        for build_type in build_types:
            for atri_key in atri_keys:
                key_tmp = "%s_%s" %(build_type,atri_key)
                if key_tmp in ret_val:
                    disp_cols.append( str(ret_val[key_tmp]) )
                else:
                    disp_cols.append("")
        
        print( "\t".join( disp_cols ) )


    
def calc_youto_chiiki():
    youto_chiiki_service = GisYoutoChiikiService()

    ret_vals = youto_chiiki_service.get_group_by_city()
    
    re_compile = re.compile(".*(住居|工業|商業).*地域")
    
    for ret_val in ret_vals:
        if not ret_val["city"]:
            continue
        
        usage_area_m2 = {"住居":0, "工業":0, "商業":0}
        
        for atri_key in ret_val.keys():
            re_result = re_compile.search(atri_key)
            if not re_result:
                continue
            usage_type = re_result.group(1)
            if ret_val[atri_key]:
                usage_area_m2[usage_type] += ret_val[atri_key]
            
        disp_cols = [
            ret_val["pref"], ret_val["city"],
            str(usage_area_m2["住居"]),
            str(usage_area_m2["工業"]),
            str(usage_area_m2["商業"]) ]

        print( "\t".join( disp_cols ) )

            

def calc_jutakutochi_d002():
    jutakutochi_service = EstatJutakuTochiD002Service()

    ret_vals = jutakutochi_service.get_vals()

    atri_keys = ["detached_house","tenement_houses","apartment",
                 "owned_house","rented_house"]

    for ret_val in ret_vals:
        disp_cols = []
        disp_cols.append( ret_val["pref"] )
        disp_cols.append( ret_val["city"] )
        
        for atri_key in atri_keys:
            if atri_key in ret_val:
                disp_cols.append( str(ret_val[atri_key] ) )
            else:
                disp_cols.append( "0" )
            
        print( "\t".join( disp_cols ) )
        
def calc_jutakutochi_e048():
    jutakutochi_service = EstatJutakuTochiE048Service()

    ret_vals = jutakutochi_service.get_shinchiku_vals_group_by_city()

    atri_keys = [
        "owner_age_24","owner_age_25_34","owner_age_35_44",
        "owner_age_45_54","owner_age_55_64","owner_age_65",
        "owner_age_unknown"]

    for ret_val in ret_vals:
        disp_cols = []
        disp_cols.append( ret_val["pref"] )
        disp_cols.append( ret_val["city"] )
        
        for atri_key in atri_keys:
            if atri_key in ret_val:
                disp_cols.append( str(ret_val[atri_key] ) )
            else:
                disp_cols.append( "0" )
            
        print( "\t".join( disp_cols ) )
        
def calc_jutakutochi_e101():
    jutakutochi_service = EstatJutakuTochiE101Service()

    ret_vals = jutakutochi_service.get_shinchiku_vals_group_by_city()

    atri_keys = [
        "buy_new","buy_used","build_new","rebuild","inheritance","other"]

    for ret_val in ret_vals:
        disp_cols = []
        disp_cols.append( ret_val["pref"] )
        disp_cols.append( ret_val["city"] )
        
        for atri_key in atri_keys:
            if atri_key in ret_val:
                disp_cols.append( str(ret_val[atri_key] ) )
            else:
                disp_cols.append( "0" )
            
        print( "\t".join( disp_cols ) )
        
def calc_jutakutochi_e049():
    jutakutochi_service = EstatJutakuTochiE049Service()

    
    ret_vals = jutakutochi_service.get_vals()

    atri_keys = ["rent_0","rent_1_9999","rent_10000_19999",
                 "rent_20000_39999","rent_40000_59999","rent_60000_79999",
                 "rent_80000_99999","rent_100000_149999","rent_150000_199999",
                 "rent_200000","rent_unknown"]

    for ret_val in ret_vals:
        disp_cols = []
        disp_cols.append( ret_val["pref"] )
        disp_cols.append( ret_val["city"] )
        disp_cols.append( ret_val["owner_age"] )
        
        for atri_key in atri_keys:
            if atri_key in ret_val:
                disp_cols.append( str(ret_val[atri_key] ) )
            else:
                disp_cols.append( "0" )
            
        print( "\t".join( disp_cols ) )
        

def calc_mlit_fudousantorihiki():
    fudousan_torihiki_service = MlitFudousanTorihikiService()

    ret_vals = fudousan_torihiki_service.get_vals_group_by_city()
    shuruis = ["宅地(土地と建物)","宅地(土地)","中古マンション等"]
    atri_keys = ["count","price"]
    tails = [None,"_pre"]
    for ret_val in ret_vals:
        disp_cols = [ret_val["pref"],ret_val["city"]]
        
        for shurui in shuruis:
            for atri_key in atri_keys:
                atri_key_now = "%s_%s" % (shurui,atri_key)
                if atri_key_now in ret_val:
                    disp_cols.append( str(ret_val[atri_key_now]))
                else:
                    disp_cols.append( "0" )
                    
                atri_key_pre = "%s_%s_pre" % (shurui,atri_key)
                if atri_key_pre in ret_val:
                    disp_cols.append( str(ret_val[atri_key_pre]))
                else:
                    disp_cols.append( "0" )

        print( "\t".join( disp_cols ) )

        
        

def calc_kokusei_pop_b02():
    kokusei_pop_b02_service = KokuseiPopulationB02Service()
    ret_vals = kokusei_pop_b02_service.get_trend()

    atri_keys = ["pop_0_4","pop_5_9","pop_10_14","pop_15_19","pop_20_24",
                 "pop_25_29","pop_30_34","pop_35_39","pop_40_44","pop_45_49",
                 "pop_50_54","pop_55_59","pop_60_64","pop_65_69","pop_70_74",
                 "pop_75_79","pop_80_84","pop_85_89","pop_90_94","pop_95_99",
                 "pop_100"]
    years = ["","_2015"]
    
    for ret_val in ret_vals:
        disp_cols = [ret_val["pref"],ret_val["city"]]
        for atri_key in atri_keys:
            for year in years:
                atri_key_tmp = atri_key + year
                disp_cols.append( str( ret_val[atri_key_tmp] ) )
            
        print( "\t".join( disp_cols ) )

def calc_kokusei_pop_b18():
    kokusei_pop_b18_service = KokuseiPopulationB18Service()
    ret_vals = kokusei_pop_b18_service.get_trend_group_by_city()

    atri_keys  = ["pref","city",
                  "owned_house",   "owned_house_2015",
                  "public_rented", "public_rented_2015",
                  "private_rented","private_rented_2015",
                  "company_house", "company_house_2015"]
    
    for ret_val in ret_vals:
        disp_cols = []
        for atri_key in atri_keys:
            disp_cols.append( str( ret_val[atri_key] ) )
            
        print( "\t".join( disp_cols ) )

        
def calc_kokusei_pop_b12():
    kokusei_pop_b12_service = KokuseiPopulationB12Service()
    ret_vals = kokusei_pop_b12_service.get_trend_group_by_city()

    atri_keys  = ["pref","city",
                  "total_setai",        "total_setai_2015",
                  "family_setai",       "family_setai_2015",
                  "other_setai",        "other_setai_2015",
                  "single_setai",       "single_setai_2015",
                  "unknown_setai",      "unknown_setai_2015" ]
    
    for ret_val in ret_vals:
        disp_cols = []
        for atri_key in atri_keys:
            disp_cols.append( str( ret_val[atri_key] ) )
            
        print( "\t".join( disp_cols ) )

        
def calc_kokusei_pop_b12_2():
    kokusei_pop_b12_service = KokuseiPopulationB12Service()
    ret_vals = kokusei_pop_b12_service.get_trend()

    atri_keys  = ["pref","city","owner_age",
                  "total_setai",        "total_setai_2015",
                  "family_setai",       "family_setai_2015",
                  "other_setai",        "other_setai_2015",
                  "single_setai",       "single_setai_2015",
                  "unknown_setai",      "unknown_setai_2015" ]
    
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
