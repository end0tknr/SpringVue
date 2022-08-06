#!python
# -*- coding: utf-8 -*-

from service.city_profile          import CityProfileService
from service.mlit_fudousantorihiki import MlitFudousanTorihikiService
from service.newbuild              import NewBuildService
from util.db import Db
import appbase
import datetime
import json
import numpy as np
import re

logger = appbase.AppBase().get_logger()

class CityNewbuildRatingService(CityProfileService):
    
    def __init__(self):
        pass
    
    def calc_save_ratings(self):
        profiles_hash = self.calc_city_profiles()
        profiles_hash = self.calc_fudousan_torihiki( profiles_hash )
        profiles_hash = self.calc_sales_count_by_city( profiles_hash )
        profiles_hash = self.calc_sales_count_by_shop( profiles_hash )

        profiles_list = self.conv_ratings_to_list(profiles_hash)
        
        util_db = Db()
        util_db.bulk_update("city_profile",
                            ["pref","city"],
                            ["pref","city","newbuild_rating"],
                            profiles_list )
        
    def calc_city_profiles(self):
        city_profile_service = CityProfileService()
        city_profiles = city_profile_service.get_all()
        
        profiles_hash = {}
        for city_profile in city_profiles:
            pref_city = city_profile["pref"] +"\t"+ city_profile["city"]
            
            profiles_hash[pref_city] = {
                "summary"           : city_profile["summary"],
                "build_year_summary": city_profile["build_year_summary"],
                "newbuild_rating"   : city_profile["newbuild_rating"] }

            profiles_hash[pref_city]["newbuild_rating"]["land_price"] = 0
            if "地価_万円_m2_住居系" in city_profile["summary"]:
                profiles_hash[pref_city]["newbuild_rating"]["land_price"] = \
                    city_profile["summary"]["地価_万円_m2_住居系"]

            for atri_key in ["家族世帯","家族世帯_変動"]:
                if atri_key in city_profile["summary"]:
                    profiles_hash[pref_city]["newbuild_rating"][atri_key] = \
                        city_profile["summary"][atri_key]

            kodate  = 0
            if "世帯_戸建" in city_profile["summary"] and \
               city_profile["summary"]["世帯_戸建"]:
                kodate = city_profile["summary"]["世帯_戸建"]
            tmp_sum = 0
            for atri_key in ["世帯_戸建","世帯_集合"]:
                if not atri_key in city_profile["summary"]:
                    continue
                tmp_sum += city_profile["summary"][atri_key]
            
            if tmp_sum :
                profiles_hash[pref_city]["newbuild_rating"]["kodate_rate"] = \
                    round(kodate/tmp_sum, 2)
            else:
                profiles_hash[pref_city]["newbuild_rating"]["kodate_rate"] = 0

            
            buy_new = 0
            if "入手_分譲" in city_profile["summary"] and \
               city_profile["summary"]["入手_分譲"]:
                buy_new = city_profile["summary"]["入手_分譲"]

            tmp_sum = 0
            for atri_key in ["入手_新築","入手_分譲","入手_建替"]:
                if not atri_key in city_profile["summary"]:
                    continue
                tmp_sum += city_profile["summary"][atri_key]

            if tmp_sum :
                profiles_hash[pref_city]["newbuild_rating"]["buy_new_rate"] = \
                    round(buy_new/tmp_sum, 2)
            else:
                profiles_hash[pref_city]["newbuild_rating"]["buy_new_rate"] = 0

        return profiles_hash

        
    def conv_ratings_to_list(self, profiles_hash):
        ret_datas = []

        for pref_city in profiles_hash.keys():
            (pref,city) = pref_city.split("\t")
            rating = profiles_hash[pref_city]["newbuild_rating"]
            rating["pref"] = pref
            rating["city"] = city
            
            ret_data = {
                "pref" : pref,
                "city" : city,
                "newbuild_rating":json.dumps(rating, ensure_ascii=False) }
            ret_datas.append( ret_data )

        return ret_datas
    
    
    def calc_sales_count_by_shop(self, profiles_hash):
        newbuild_service = NewBuildService()
        sales_counts = newbuild_service.get_newest_sales_count_by_shop_city()
        # 差値算出用
        standard_score ={
            "onsale_shop":{"scores":[],"no_scores":[],"mean":None,"std":None} }

        for sales_count in sales_counts:
            pref_city = sales_count["pref"] +"\t"+ sales_count["city"]

            if not pref_city in profiles_hash or \
               not "sold_count" in profiles_hash[pref_city]["newbuild_rating"]:
                continue
            
            sold_count = profiles_hash[pref_city]["newbuild_rating"]["sold_count"]
            profiles_hash[pref_city]["newbuild_rating"]["onsale_shop"] = \
                sales_count["shop"]
            
            for atri_key,ss_score in standard_score.items():
                ss_score["scores"].append(
                    sold_count/profiles_hash[pref_city][
                        "newbuild_rating"]["onsale_shop"])
                
        for atri_key,ss_score in standard_score.items():
            ss_score["np_scores"] = np.array( ss_score["scores"] )
            ss_score["mean"] = np.mean(ss_score["np_scores"] ) # 平均
            ss_score["std"]  = np.std( ss_score["np_scores"] ) # 標準偏差

        for pref_city, profile_tmp in profiles_hash.items():

            if not "sold_count" in profiles_hash[pref_city]["newbuild_rating"]:
                continue
            sold_count = profiles_hash[pref_city]["newbuild_rating"]["sold_count"]
            
            for atri_key,ss_score in standard_score.items():
                if not atri_key in profile_tmp["newbuild_rating"]:
                    continue
                tmp_mean  = ss_score["mean"]
                tmp_std   = ss_score["std"]
                tmp_count = sold_count / profile_tmp["newbuild_rating"][atri_key]
                
                # 偏差値算出
                profile_tmp["newbuild_rating"]["ss_"+atri_key] = \
                    round( (tmp_count - tmp_mean) / tmp_std * 10 + 50 )
        return profiles_hash

        
    def calc_sales_count_by_city(self, profiles_hash):
        newbuild_service = NewBuildService()
        sales_counts = newbuild_service.get_newest_sales_count_by_city()
        
        for sales_count in sales_counts:
            pref_city = sales_count["pref"] +"\t"+ sales_count["city"]

            if not pref_city in profiles_hash:
                continue

            profiles_hash[pref_city]["newbuild_rating"]["discuss_days"] = 0
            if sales_count["discuss_days"]:
                profiles_hash[pref_city]["newbuild_rating"]["discuss_days"] = \
                    round(10 / sales_count["discuss_days"],2)

            onsale_count = sales_count["onsale_count"]
            if not onsale_count:
                continue
            
            if not "sold_count" in profiles_hash[pref_city]["newbuild_rating"]:
                continue
            
            sold_count = profiles_hash[pref_city]["newbuild_rating"]["sold_count"]
            profiles_hash[pref_city]["newbuild_rating"]["sold_onsale_count"] = \
                round(sold_count*10 / onsale_count,2)
        return profiles_hash

        
    def calc_fudousan_torihiki(self, profiles_hash):
        fudousan_torihiki_service = MlitFudousanTorihikiService()

        # 6ケ月前を基準に、年度の販売棟数を取得
        tmp_date = datetime.date.today() - datetime.timedelta(days=(30*6))
        pre_year = tmp_date.year
        if  1<=tmp_date.month and tmp_date.month<=3:
            pre_year -= 1

        years = [pre_year-1, pre_year]
        fudousan_torihikis = \
            fudousan_torihiki_service.get_city_years("newbuild",years )

        sold_counts = []
        for fudousan_torihiki in fudousan_torihikis:
            pref_city = fudousan_torihiki["pref"] +"\t"+ fudousan_torihiki["city"]

            if not pref_city in profiles_hash:
                continue

            buy_new_rate = \
                profiles_hash[pref_city]["newbuild_rating"]["buy_new_rate"]

            count_new = "sold_count_" + str(years[1])
            price_new = "sold_price_" + str(years[1])
            count_pre = "sold_count_" + str(years[0])

            profiles_hash[pref_city]["newbuild_rating"]["sold_count"] = 0
            if count_new in fudousan_torihiki:
                profiles_hash[pref_city]["newbuild_rating"]["sold_count"] = \
                    round(fudousan_torihiki[count_new] * buy_new_rate,1)

            # 以下の 1000は、標準偏差算出で桁溢れ?を防ぐ為のものです
            sold_counts.append(
                profiles_hash[pref_city]["newbuild_rating"]["sold_count"] * 1000 / \
                profiles_hash[pref_city]["summary"]["家族世帯"])

            profiles_hash[pref_city]["newbuild_rating"]["sold_price"] = 0
            if price_new in fudousan_torihiki:
                profiles_hash[pref_city]["newbuild_rating"]["sold_price"] = \
                    round(fudousan_torihiki[price_new] / 1000000)
                
            if count_pre in fudousan_torihiki:
                profiles_hash[pref_city]["newbuild_rating"]["sold_count_diff"] = \
                    profiles_hash[pref_city]["newbuild_rating"]["sold_count"] - \
                    fudousan_torihiki[count_pre] * buy_new_rate
                profiles_hash[pref_city]["newbuild_rating"]["sold_count_diff"] = \
                    round(profiles_hash[pref_city]["newbuild_rating"]["sold_count_diff"],1)
                
        np_scores = np.array( sold_counts )
        tmp_mean = np.mean(np_scores)   # 平均
        tmp_std = np.std( sold_counts ) # 標準偏差
        
        for pref_city, profile_tmp in profiles_hash.items():
            if not "sold_count" in profile_tmp["newbuild_rating"]:
                continue
            
            # 以下の 1000は、標準偏差算出で桁溢れ?を防ぐ為のものです
            tmp_count = \
                profile_tmp["newbuild_rating"]["sold_count"] * 1000 / \
                profile_tmp["summary"]["家族世帯"]
            # 偏差値算出
            profile_tmp["newbuild_rating"]["ss_sold_count"] = \
                round( (tmp_count - tmp_mean) / tmp_std * 10 + 50 )

        return profiles_hash
