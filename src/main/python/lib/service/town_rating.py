#!python
# -*- coding: utf-8 -*-

from service.city_profile import CityProfileService
from service.town         import TownService
import appbase

logger = appbase.AppBase().get_logger()

class TownRatingService(TownService):
    
    def __init__(self):
        pass


    def calc_save_ratings(self):
        profiles_hash = self.calc_town_profiles()
        profiles_hash = self.calc_city_profiles( profiles_hash )
        profiles_hash = self.calc_fudousan_torihiki( profiles_hash )


    def calc_fudousan_torihiki(self, profiles_hash):
        fudousan_torihiki_service = MlitFudousanTorihikiService()
        
        # 6ケ月前を基準に、年度の販売棟数を取得
        tmp_date = datetime.date.today() - datetime.timedelta(days=(30*6))
        pre_year = tmp_date.year
        if  1<=tmp_date.month and tmp_date.month<=3:
            pre_year -= 1

        year_q = [pre_year*10+1,pre_year*10+4]
        fudousan_torihikis = \
            fudousan_torihiki_service.get_town_sumed_summaries("newbuild",
                                                               year_q )
        for fudousan_torihiki in fudousan_torihikis:
            pref_city_town = "\t".join([fudousan_torihiki["pref"],
                                        fudousan_torihiki["city"],
                                        fudousan_torihiki["town"] ])

            if not pref_city_town in profiles_hash:
                continue

            sold_count = fudousan_torihiki["sold_count"]
            buy_new_rate = profiles_hash[pref_city_town]["rating"]["buy_new_rate"]

            profiles_hash[pref_city_town]["rating"]["sold_count"] = \
                round(sold_count * buy_new_rate,1)

            family_setai = profiles_hash[pref_city]["summary"]["家族世帯"]

            profiles_hash[pref_city]["rating"]["sold_x_family_setai"] = \
                round(sold_count * 1000 / family_setai,2)

        return profiles_hash


    def calc_city_profiles(self, profiles_hash):
        city_profile_service = CityProfileService()
        city_profiles = city_profile_service.get_all()

        city_profiles_hash = {}
        for city_profile in city_profiles:
            pref_city = city_profile["pref"] +"\t"+ city_profile["city"]

            city_profiles_hash[pref_city] = {
                "summary"           : city_profile["summary"],
                "build_year_summary": city_profile["build_year_summary"],
                "rating"            : city_profile["rating"] }

        for pref_city_town in profiles_hash:
            (pref,city,town) = pref_city_town.split("\t")
            pref_city = pref +"\t"+ "city"
            
            if pref_city in city_profiles_hash and \
               "buy_new_rate" in city_profiles_hash[pref_city]["rating"]:
                profiles_hash[pref_city_town]["rating"]["buy_new_rate"] = \
                    city_profiles_hash[pref_city]["rating"]["buy_new_rate"]
                
        return profiles_hash
                
        
    def calc_town_profiles(self):
        town_service = TownService()
        town_profiles = town_service.get_all()

        profiles_hash = {}
        for town_profile in town_profiles:
            pref_city_town = "\t".join([town_profile["pref"],
                                        town_profile["city"],
                                        town_profile["town"] ])

            profiles_hash[pref_city_town] = {
                "summary":town_profile["summary"], "rating":{} }


            for atri_key in ["pop_2020_25_59","pop_diff_25_59"]:
                if not atri_key in town_profile["summary"]:
                    continue
            
                profiles_hash[pref_city_town]["rating"][atri_key] = \
                    town_profile["summary"][atri_key]
        return profiles_hash
