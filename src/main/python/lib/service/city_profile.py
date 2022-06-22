#!python
# -*- coding: utf-8 -*-

from service.city                   import CityService
from service.estat_jutakutochi_d002 import EstatJutakuTochiD002Service
from service.gis_chika_koji         import GisChikaKojiService
from service.gis_youto_chiiki       import GisYoutoChiikiService
from service.kokusei_population_b01 import KokuseiPopulationB01Service
from service.kokusei_population_b02 import KokuseiPopulationB02Service
from service.kokusei_population_b12 import KokuseiPopulationB12Service
from service.mlit_seisanryokuchi    import MlitSeisanRyokuchiService
from service.soumu_zeisei_j5120b    import SoumuZeiseiJ5120bService
import appbase
import json
import re

logger = None


class CityProfileService(appbase.AppBase):
    
    def __init__(self):
        global logger
        logger = self.get_logger()

    def save_profiles(self,profiles):
        logger.info("start")

        sql = """
INSERT INTO city_profile (pref,city,summary)
VALUES (%s,%s,%s)
"""
        db_conn = self.db_connect()
        with self.db_cursor(db_conn) as db_cur:
            for profile in profiles:
                sql_args = (profile["pref"],
                            profile["city"],
                            json.dumps( profile, ensure_ascii=False) )
            
                try:
                    db_cur.execute(sql, sql_args)
                    db_conn.commit()
                except Exception as e:
                    logger.error(e)
                    logger.error(sql)
                    logger.error(sql_args)
                    return False
        return True
        
    def calc_profiles(self):
        logger.info("start")

        profiles = self.make_profile_base()

        # 総人口
        profiles = self.calc_population_setai(profiles)
        # 年代別実行
        profiles = self.calc_kokusei_pop_b02(profiles)
        # 同居形態
        profiles = self.calc_kokusei_pop_b12(profiles)
        # 用途地域
        profiles = self.calc_youto_chiiki(profiles)
        # 生産緑地
        profiles = self.calc_mlit_seisanryokuchi(profiles)
        # 地価
        profiles = self.calc_chika_koji(profiles)
        # 戸建/集合、持家/賃貸
        profiles = self.calc_jutakutochi_d002(profiles)
        # 年収
        profiles = self.calc_soumu_zeisei(profiles)

        ret_datas = []
        for pref_city, profile in profiles.items():
            (profile["pref"],profile["city"]) = pref_city.split("\t")
            ret_datas.append( profile )
        return ret_datas
        
    def make_profile_base(self):
        city_service = CityService()
        org_cities = city_service.get_all()
        
        ret_datas = {}
        for org_city in org_cities:
            if not org_city["city"]:
                continue

            if city_service.is_seirei_city(org_city["city"]) and \
               org_city["city"][-1] == "市":
                continue

            pref_city = org_city["pref"] +"\t"+ org_city["city"]
            ret_datas[pref_city] = {}
        return ret_datas
        
        
    def calc_population_setai(self,profiles):
        # 総人口
        kokusei_pop_b01_service = KokuseiPopulationB01Service()
        ret_vals = kokusei_pop_b01_service.get_group_by_city()
        
        for ret_val in ret_vals:
            pref_city = ret_val["pref"]+"\t"+ret_val["city"]
            if not pref_city in profiles:
                logger.warning("%s not exist" % (pref_city,) )
                continue
            
            profiles[pref_city]["総人口_万人"]     = \
                round( ret_val["pop"]/10000, 1)
            profiles[pref_city]["総人口_万人_2015"]= \
                round( ret_val["pop_2015"]/10000,1)

        return profiles

    def calc_kokusei_pop_b02(self, profiles):
        kokusei_pop_b02_service = KokuseiPopulationB02Service()
        ret_vals = kokusei_pop_b02_service.get_trend()

        years = ["","_2015"]
        atri_keys_20_29 = ["pop_20_24","pop_25_29"]
        atri_keys_30_59 = ["pop_30_34","pop_35_39",
                           "pop_40_44","pop_45_49",
                           "pop_50_54","pop_55_59"]
        for ret_val in ret_vals:
            pref_city = ret_val["pref"]+"\t"+ret_val["city"]
            if not pref_city in profiles:
                logger.warning("%s not exist" % (pref_city,) )
                continue
            
            for year in years:
                tmp_val = 0
                for atri_key in atri_keys_20_29:
                    tmp_val += ret_val[atri_key]

                profiles[pref_city]["人口_20_29歳_万人"+year] = \
                round( tmp_val / 10000,1)
                
                tmp_val = 0
                for atri_key in atri_keys_30_59:
                    tmp_val += ret_val[atri_key]

                profiles[pref_city]["人口_30_59歳_万人"+year] = \
                round( tmp_val / 10000,1)
        return profiles


    def calc_kokusei_pop_b12(self, profiles):
        kokusei_pop_b12_service = KokuseiPopulationB12Service()
        ret_vals = kokusei_pop_b12_service.get_trend_group_by_city()

        atri_keys  = ["total_setai",        "total_setai_2015",
                      "family_setai",       "family_setai_2015",
                      "single_setai",       "single_setai_2015"]

        for ret_val in ret_vals:
            pref_city = ret_val["pref"]+"\t"+ret_val["city"]
            if not pref_city in profiles:
                logger.warning("%s not exist" % (pref_city,) )
                continue

            for year in ["","_2015"]:
                profiles[pref_city]["総世帯"+year] = \
                    int( ret_val["total_setai"+year])
                profiles[pref_city]["家族世帯"+year] = \
                    int( ret_val["family_setai"+year] )
                profiles[pref_city]["単身世帯"+year] = \
                    int( ret_val["single_setai"+year])
        return profiles
        
        
    def calc_youto_chiiki(self, profiles):
        youto_chiiki_service = GisYoutoChiikiService()

        ret_vals = youto_chiiki_service.get_group_by_city()

        re_compile = re.compile(".*(住居|工業|商業).*地域")
        usages = [
            "第一種低層住居専用地域",   "第二種低層住居専用地域",
            "第一種中高層住居専用地域", "第二種中高層住居専用地域",
            "第一種住居地域",           "第二種住居地域",  "準住居地域",
            "商業地域",                 "近隣商業地域",
            "工業地域",                 "工業専用地域",    "準工業地域"]

        for ret_val in ret_vals:
            if not ret_val["city"]:
                continue
            
            pref_city = ret_val["pref"]+"\t"+ret_val["city"]
            if not pref_city in profiles:
                logger.warning("%s not exist" % (pref_city,) )
                continue

            usage_area_m2 = {"住居":0, "工業":0, "商業":0}

            for atri_key in ret_val.keys():
                re_result = re_compile.search(atri_key)
                if not re_result:
                    continue
                usage_type = re_result.group(1)
                if ret_val[atri_key]:
                    usage_area_m2[usage_type] += ret_val[atri_key]

            if not pref_city in profiles:
                profiles[pref_city] = {}
                
            profiles[pref_city]["用途地域_住居系_ha"] = \
                int( usage_area_m2["住居"]/10000)
            profiles[pref_city]["用途地域_工業系_ha"] = \
                int( usage_area_m2["工業"]/10000)
            profiles[pref_city]["用途地域_商業系_ha"] = \
                int( usage_area_m2["商業"]/10000)
        return profiles
    
    
    def calc_mlit_seisanryokuchi(self, profiles):
        seisanryokuchi_service = MlitSeisanRyokuchiService()

        ret_vals = seisanryokuchi_service.get_vals()

        for ret_val in ret_vals:
            pref_city = ret_val["pref"]+"\t"+ret_val["city"]
            if not pref_city in profiles:
                logger.warning("%s not exist" % (pref_city,) )
                continue
                
            profiles[pref_city]["生産緑地_ha"] = ret_val["area_ha"]
        return profiles

    def calc_chika_koji(self, profiles):
        chika_koji_service = GisChikaKojiService()

        ret_vals = chika_koji_service.get_union_vals()
        for ret_val in ret_vals:
            pref_city = ret_val["pref"]+"\t"+ret_val["city"]
            if not pref_city in profiles:
                logger.warning("%s not exist" % (pref_city,) )
                continue

            for atri_key in ["住居系","商業系"]:
                if atri_key in ret_val:
                    profiles[pref_city]["地価_千円_m2_"+atri_key] = \
                        int(ret_val[atri_key]/1000)
        return profiles

    
    def calc_jutakutochi_d002(self, profiles):
        jutakutochi_service = EstatJutakuTochiD002Service()

        ret_vals = jutakutochi_service.get_vals()

        for ret_val in ret_vals:
            pref_city = ret_val["pref"]+"\t"+ret_val["city"]
            if not pref_city in profiles:
                logger.warning("%s not exist" % (pref_city,) )
                continue
                
            profiles[pref_city]["世帯_戸建"] = ret_val["detached_house"]
            profiles[pref_city]["世帯_集合"] = ret_val["apartment"]
            profiles[pref_city]["世帯_持家"] = ret_val["owned_house"]
            profiles[pref_city]["世帯_賃貸"] = ret_val["rented_house"]
        return profiles

        
    def calc_soumu_zeisei(self, profiles):
        soumu_zeisei = SoumuZeiseiJ5120bService()
        ret_vals = soumu_zeisei.get_vals()
        
        for ret_val in ret_vals:
            pref_city = ret_val["pref"]+"\t"+ret_val["city"]
            if not pref_city in profiles:
                logger.warning("%s not exist" % (pref_city,) )
                continue
                
            profiles[pref_city]["給与年収_万円"] = \
                int(ret_val["salary"]/10000)
            profiles[pref_city]["資産年収_万円"] = \
                int(ret_val["capital_income"]/10000)
        return profiles


