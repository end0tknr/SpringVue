#!python
# -*- coding: utf-8 -*-

from service.city                   import CityService
from service.estat_jutakutochi_d002 import EstatJutakuTochiD002Service
from service.estat_jutakutochi_e033 import EstatJutakuTochiE033Service
from service.estat_jutakutochi_e044 import EstatJutakuTochiE044Service
from service.estat_jutakutochi_e048 import EstatJutakuTochiE048Service
from service.estat_jutakutochi_e101 import EstatJutakuTochiE101Service
from service.estat_jutakutochi_g157 import EstatJutakuTochiG157Service
from service.gis_chika_koji         import GisChikaKojiService
from service.gis_youto_chiiki       import GisYoutoChiikiService
from service.kokusei_population_b01 import KokuseiPopulationB01Service
from service.kokusei_population_b02 import KokuseiPopulationB02Service
from service.kokusei_population_b12 import KokuseiPopulationB12Service
from service.mlit_seisanryokuchi    import MlitSeisanRyokuchiService
from service.soumu_zeisei_j5120b    import SoumuZeiseiJ5120bService
import appbase
import dictknife
import json
import re

logger = appbase.AppBase().get_logger()

class CityProfileService(appbase.AppBase):
    
    def __init__(self):
        pass

    def del_profiles(self):
        logger.info("start")

        sql = """
DELETE FROM city_profile
"""
        db_conn = self.db_connect()
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute(sql)
                db_conn.commit()
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return False
        return True
        
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
        
    def get_all(self):

        sql = """
SELECT * from city_profile
"""
        db_conn = self.db_connect()
        with self.db_cursor(db_conn) as db_cur:
            try:
                db_cur.execute(sql)
            except Exception as e:
                logger.error(e)
                logger.error(sql)
                return []
            
            ret_datas = []
            for ret_row in  db_cur.fetchall():
                ret_row = dict( ret_row )
                for atri_key in ["summary","newbuild_rating"]:
                    if ret_row[atri_key]:
                        ret_row[atri_key] = json.loads( ret_row[atri_key] )
                    else:
                        ret_row[atri_key] = {}
                        
                atri_key = "build_year_summary"
                if ret_row[atri_key]:
                    ret_row[atri_key] = json.loads( ret_row[atri_key] )
                else:
                    ret_row[atri_key] = []
                        
                ret_datas.append( ret_row )
            return ret_datas
        
        
    def calc_profiles(self):
        logger.info("start")

        profiles = self.make_profile_base()

        # 総人口
        profiles = self.calc_population_setai(profiles)
        # 年代別人口
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
        # 入手方法
        profiles = self.calc_jutakutochi_e101_recenct(profiles)
        # 年収
        profiles = self.calc_soumu_zeisei(profiles)
        # 世帯年収
        # profiles = self.calc_jutakutochi_e044(profiles)
        # 新築 世帯主年齢
        # profiles = self.calc_jutakutochi_e048(profiles)
        
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
            ret_datas[pref_city] = {"citycode":org_city["code"],
                                    "lng":org_city["lng"],
                                    "lat":org_city["lat"] }
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
                round( ret_val["pop"]/10000, 2)
            profiles[pref_city]["総人口_万人_2015"]= \
                round( ret_val["pop_2015"]/10000,2)
        return profiles
    
    # def calc_jutakutochi_e044(self,profiles):
    #     jutakutochi_service = EstatJutakuTochiE044Service()

    #     ret_vals = jutakutochi_service.get_group_by_city_income()

    #     for ret_val in ret_vals:
    #         pref_city = ret_val["pref"]+"\t"+ret_val["city"]
    #         if not pref_city in profiles:
    #             logger.warning("%s not exist" % (pref_city,) )
    #             continue

    #         if not "持ち家" in ret_val:
    #             continue

    #         income = ret_val["year_income"]
    #         income = income.replace('万円未満','').replace('万円以上','')
            
    #         profiles[pref_city]["世帯年収_"+income ] = ret_val["持ち家"]
    #     return profiles

    # def calc_jutakutochi_e048(self,profiles):
    #     jutakutochi_service = EstatJutakuTochiE048Service()

    #     ret_vals = jutakutochi_service.get_shinchiku_vals_group_by_city()

    #     for ret_val in ret_vals:
    #         pref_city = ret_val["pref"]+"\t"+ret_val["city"]
    #         if not pref_city in profiles:
    #             logger.warning("%s not exist" % (pref_city,) )
    #             continue

    #         for age_key in ["24","25_34","35_44","45_54","55_64","65"]:
    #             tmp_key_1 = "新築_世帯主_年齢_%s" % (age_key,)
    #             tmp_key_2 = "owner_age_%s"        % (age_key,)

    #             profiles[pref_city][tmp_key_1]    = ret_val[tmp_key_2]
    #     return profiles

    def calc_jutakutochi_e101_recenct(self, profiles):
        jutakutochi_service = EstatJutakuTochiE101Service()

        ret_vals = jutakutochi_service.get_shinchiku_vals_group_by_city()

        for ret_val in ret_vals:
            pref_city = ret_val["pref"]+"\t"+ret_val["city"]
            if not pref_city in profiles:
                logger.warning("%s not exist" % (pref_city,) )
                continue

            profiles[pref_city]["入手_新築"] = ret_val["build_new"]
            profiles[pref_city]["入手_分譲"] = ret_val["buy_new"]
            profiles[pref_city]["入手_建替"] = ret_val["rebuild"]
        return profiles
    

    def calc_kokusei_pop_b02(self, profiles):
        kokusei_pop_b02_service = KokuseiPopulationB02Service()
        ret_vals = kokusei_pop_b02_service.get_trend()

        years = ["","_2015"]
        atri_keys_20_24 = ["pop_20_24",]
        atri_keys_25_59 = ["pop_25_29","pop_30_34","pop_35_39",
                           "pop_40_44","pop_45_49","pop_50_54","pop_55_59"]
        atri_keys_60 = ["pop_60_64","pop_65_69","pop_70_74","pop_75_79",
                        "pop_80_84","pop_85_89","pop_90_94","pop_95_99",
                        "pop_100"]
        for ret_val in ret_vals:
            pref_city = ret_val["pref"]+"\t"+ret_val["city"]
            if not pref_city in profiles:
                logger.warning("%s not exist" % (pref_city,) )
                continue
            
            for year in years:
                tmp_val = 0
                for atri_key in atri_keys_20_24:
                    tmp_val += ret_val[atri_key+year]
                profiles[pref_city]["人口_20_24歳_万人"+year] = \
                    round( tmp_val / 10000,2)
                
                tmp_val = 0
                for atri_key in atri_keys_25_59:
                    tmp_val += ret_val[atri_key+year]
                profiles[pref_city]["人口_25_59歳_万人"+year] = \
                    round( tmp_val / 10000,2)
                
                tmp_val = 0
                for atri_key in atri_keys_60:
                    tmp_val += ret_val[atri_key+year]
                profiles[pref_city]["人口_60歳_万人"+year] = \
                    round( tmp_val / 10000,2)

            profiles[pref_city]["人口_25_59歳_万人_変動"] = \
                profiles[pref_city]["人口_25_59歳_万人"] - \
                profiles[pref_city]["人口_25_59歳_万人_2015"]
            profiles[pref_city]["人口_25_59歳_万人_変動"] = \
                round( profiles[pref_city]["人口_25_59歳_万人_変動"], 2)
                
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

                for setai_key in [["家族世帯","family_setai"],
                                  ["単身世帯","single_setai"]]:
                    profiles[pref_city][setai_key[0]+year] = \
                        int( ret_val[setai_key[1]+year] )

                    if setai_key[0]+"_2015" in profiles[pref_city]:
                        profiles[pref_city][setai_key[0] +"_変動"] = \
                            profiles[pref_city][setai_key[0]] - \
                            profiles[pref_city][setai_key[0]+"_2015"]
                        profiles[pref_city][setai_key[0] +"_変動"] = \
                            round( profiles[pref_city][setai_key[0] +"_変動"], 2)
                    else:
                        profiles[pref_city][setai_key[0] +"_変動"] = 0
                    
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

            for area_key in ["住居","工業","商業"]:
                area_key_2 = "用途地域_%s系_ha" % (area_key,)
                
                profiles[pref_city][area_key_2] = \
                    int( usage_area_m2[area_key]/10000)
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
                    profiles[pref_city]["地価_万円_m2_"+atri_key] = \
                        int(ret_val[atri_key]/10000)
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

            tmp_val = ret_val["salary"] + ret_val["capital_income"]
            profiles[pref_city]["年収_百万円"] = round( tmp_val/1000000, 2)
            
        return profiles
    

    def calc_save_bild_year_profiles(self):
        
        profiles = self.get_bild_year_defaults()

        # 築年数と損傷有無
        profiles = self.calc_jutakutochi_e033(profiles)
        # 築年数と建替え等
        profiles = self.calc_jutakutochi_e101(profiles)
        # 築年数とリフォーム
        profiles = self.calc_jutakutochi_g157(profiles)

        profiles_tmp = self.conv_build_year_profiles( profiles )

        self.save_build_year_profiles(profiles_tmp)
        
        
    def save_build_year_profiles(self,profiles):
        logger.info("start")

        sql = """
UPDATE city_profile
SET build_year_summary = %s
WHERE pref=%s AND city=%s
"""
        db_conn = self.db_connect()
        with self.db_cursor(db_conn) as db_cur:
            for profile in profiles:
                sql_args = (profile["build_year_summary"],
                            profile["pref"],
                            profile["city"] )
            
                try:
                    db_cur.execute(sql, sql_args)
                except Exception as e:
                    logger.error(e)
                    logger.error(sql)
                    logger.error(sql_args)
                    return False
            try:
                db_conn.commit()
            except Exception as e:
                logger.error(e)
                return False
            
        return True

        
    def conv_build_year_profiles(self, profiles):
        
        profiles_tmp = []
        for pref_city_str, profile_tmp_1 in profiles.items():
            pref_city = pref_city_str.split("\t")

            profile_tmp = {"pref":pref_city[0],
                           "city":pref_city[1],
                           "build_year_summary":[] }
            
            for build_year_str, profile_tmp_2 in profile_tmp_1.items():
                build_years = build_year_str.split("\t")
                if len(build_years) != 2:
                    logger.error(build_year_str)
                    logger.error(profile_tmp_2)
                    continue

                profile_tmp_2["build_year_from"] = build_years[0]
                profile_tmp_2["build_year_to"]   = build_years[1]

                profile_tmp["build_year_summary"].append( profile_tmp_2 )

            json_str = json.dumps( profile_tmp["build_year_summary"],
                                   ensure_ascii=False )
            
            profiles_tmp.append({"pref" : pref_city[0],
                                 "city" : pref_city[1],
                                 "build_year_summary": json_str })
        return profiles_tmp
        

    def get_bild_year_defaults(self):
        city_serivce = CityService()
        cities = city_serivce.get_all()

        ret_datas = {}
        
        for city in cities:
            if not city["city"]:
                continue
            
            pref_city = city["pref"] +"\t"+ city["city"]
            ret_datas[pref_city] = {}
            
            # for build_year in default_build_years:
            #     year_from_to = str(build_year[0]) +"\t"+ str(build_year[1])
            #     ret_datas[pref_city][year_from_to] = {}
                
        return ret_datas
    

    def calc_jutakutochi_e033(self,profiles):
        jutakutochi_service = EstatJutakuTochiE033Service()

        ret_vals = jutakutochi_service.get_group_by_city()

        for ret_val in ret_vals:
            pref_city = ret_val["pref"]+"\t"+ret_val["city"]
            del ret_val["pref"]
            del ret_val["city"]
            
            if not pref_city in profiles:
                profiles[pref_city] = {}

            profiles[pref_city] = dictknife.deepmerge(profiles[pref_city],
                                                      ret_val )
        return profiles
    
    
    def calc_jutakutochi_e101(self, profiles):
        jutakutochi_service = EstatJutakuTochiE101Service()

        ret_vals = jutakutochi_service.get_group_by_city()

        for ret_val in ret_vals:
            pref_city = ret_val["pref"]+"\t"+ret_val["city"]
            del ret_val["pref"]
            del ret_val["city"]
            
            if not pref_city in profiles:
                profiles[pref_city] = {}

            profiles[pref_city] = dictknife.deepmerge(profiles[pref_city],
                                                      ret_val )
            
        return profiles
        
    def calc_jutakutochi_g157(self, profiles):
        jutakutochi_service = EstatJutakuTochiG157Service()

        ret_vals = jutakutochi_service.get_group_by_city()

        for ret_val in ret_vals:
            pref_city = ret_val["pref"]+"\t"+ret_val["city"]
            del ret_val["pref"]
            del ret_val["city"]
            
            if not pref_city in profiles:
                profiles[pref_city] = {}

            profiles[pref_city] = dictknife.deepmerge(profiles[pref_city],
                                                      ret_val )
        return profiles
        
