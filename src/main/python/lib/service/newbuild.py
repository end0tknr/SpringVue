#!python
# -*- coding: utf-8 -*-

from service.suumo import SuumoService
from util.db import Db
import appbase
import datetime
import re

logger = None

class NewBuildService(appbase.AppBase):

    def __init__(self):
        global logger
        logger = self.get_logger()

    def calc_save_sales_count_by_shop_sub(self,
                                          ret_datas_tmp,
                                          calc_key,
                                          calc_date_from,
                                          calc_date_to):
        
        suumo_service = SuumoService()
        org_bukkens = suumo_service.get_bukkens_by_check_date("新築戸建",
                                                              calc_date_from,
                                                              calc_date_to)
        for org_bukken in org_bukkens:
            if not org_bukken["pref"]:
                org_bukken["pref"] = "?"
            if not org_bukken["shop"]:
                org_bukken["shop"] = "?"

            pref_shop = "%s\t%s" % (org_bukken["pref"],org_bukken["shop"])

            if not pref_shop in ret_datas_tmp:
                ret_datas_tmp[pref_shop] = {
                    "calc_date" : str(calc_date_to),
                    "calc_days" : 7,
                    "sold_count": 0,
                    "sold_price": 0,
                    "sold_days" : 0,
                    "on_sale_count":0,
                    "on_sale_price":0,
                    "on_sale_days" :0 }


            ret_datas_tmp[pref_shop][calc_key+"_count"] += 1
            if org_bukken["price"]:
                ret_datas_tmp[pref_shop][calc_key+"_price"] += org_bukken["price"]

            tmp_days = org_bukken["check_date"] - org_bukken["found_date"]
            ret_datas_tmp[pref_shop][calc_key+"_days"] += tmp_days.days

        return ret_datas_tmp
        
    def calc_save_sales_count_by_shop(self):
        logger.info("start")
        
        today = datetime.datetime.today().date()
        calc_date_from, calc_date_to = self.get_weekly_period(today)

        ret_datas_tmp = self.calc_sales_count_by_shop_sub({},
                                                          "on_sale",
                                                          calc_date_from,
                                                          calc_date_to)
        
        calc_date_from, calc_date_to = \
            self.get_weekly_period( today - datetime.timedelta(days= 7) )

        ret_datas_tmp = self.calc_sales_count_by_shop_sub(ret_datas_tmp,
                                                          "sold",
                                                          calc_date_from,
                                                          calc_date_to)
        
        ret_datas = []
        for pref_shop, shop_info in ret_datas_tmp.items():
            (shop_info["pref"],shop_info["shop"]) = pref_shop.split("\t")

            for calc_key in ["on_sale","sold"]:
                count_key = calc_key+"_count"
                price_key = calc_key+"_price"
                days_key  = calc_key+"_price"
                
                if not shop_info[count_key]:
                    continue

                shop_info[price_key] = \
                    shop_info[price_key] / shop_info[count_key]
                shop_info[days_key] = \
                    shop_info[days_key] / shop_info[count_key]

            ret_datas.append(shop_info)

        util_db = Db()
        util_db.save_tbl_rows("newbuild_sales_count_by_shop",
                              ["pref","shop","calc_date","calc_days",
                               "sold_count",   "sold_price",   "sold_days",
                               "on_sale_count","on_sale_price","on_sale_days"],
                              ret_datas)
        return ret_datas

    def calc_save_sales_count_by_city(self):
        logger.info("start")
        
        today = datetime.datetime.today().date()
        calc_date_from, calc_date_to = self.get_weekly_period(today)

        ret_datas_tmp = self.calc_sales_count_by_city_sub({},
                                                          "on_sale",
                                                          calc_date_from,
                                                          calc_date_to)
        
        calc_date_from, calc_date_to = \
            self.get_weekly_period( today - datetime.timedelta(days= 7) )

        ret_datas_tmp = self.calc_sales_count_by_city_sub(ret_datas_tmp,
                                                          "sold",
                                                          calc_date_from,
                                                          calc_date_to)
        
        ret_datas = []
        for pref_city, city_info in ret_datas_tmp.items():
            (city_info["pref"],city_info["city"]) = pref_city.split("\t")

            for calc_key in ["on_sale","sold"]:
                count_key = calc_key+"_count"
                price_key = calc_key+"_price"
                days_key  = calc_key+"_price"
                
                if not city_info[count_key]:
                    continue

                city_info[price_key] = \
                    city_info[price_key] / city_info[count_key]
                city_info[days_key] = \
                    city_info[days_key] / city_info[count_key]

            ret_datas.append(city_info)

        util_db = Db()
        util_db.save_tbl_rows("newbuild_sales_count_by_city",
                              ["pref","city","calc_date","calc_days",
                               "sold_count",   "sold_price",   "sold_days",
                               "on_sale_count","on_sale_price","on_sale_days"],
                              ret_datas)
        return ret_datas

    def calc_sales_count_by_city_sub(self,
                                     ret_datas_tmp,
                                     calc_key,
                                     calc_date_from,
                                     calc_date_to):
        
        suumo_service = SuumoService()
        org_bukkens = suumo_service.get_bukkens_by_check_date("新築戸建",
                                                              calc_date_from,
                                                              calc_date_to)
        for org_bukken in org_bukkens:
            if not org_bukken["pref"]:
                org_bukken["pref"] = "?"
            if not org_bukken["city"]:
                org_bukken["city"] = "?"

            pref_city = "%s\t%s" % (org_bukken["pref"],org_bukken["city"])

            if not pref_city in ret_datas_tmp:
                ret_datas_tmp[pref_city] = {
                    "calc_date" : str(calc_date_to),
                    "calc_days" : 7,
                    "sold_count": 0,
                    "sold_price": 0,
                    "sold_days" : 0,
                    "on_sale_count":0,
                    "on_sale_price":0,
                    "on_sale_days" :0 }


            ret_datas_tmp[pref_city][calc_key+"_count"] += 1
            if org_bukken["price"]:
                ret_datas_tmp[pref_city][calc_key+"_price"] += org_bukken["price"]

            tmp_days = org_bukken["check_date"] - org_bukken["found_date"]
            ret_datas_tmp[pref_city][calc_key+"_days"] += tmp_days.days

        return ret_datas_tmp
        
            
    def get_weekly_period(self,today):
        weekday = today.weekday() # 0=Mon ... 6=Sun
        calc_date_from = today - datetime.timedelta(days= weekday  ) # Mon
        calc_date_to   = today + datetime.timedelta(days= 6-weekday) # Sun
        return calc_date_from, calc_date_to


    def calc_save_sales_count_by_town(self):
        logger.info("start")
        
        today = datetime.datetime.today().date()
        calc_date_from, calc_date_to = self.get_weekly_period(today)

        ret_datas_tmp = self.calc_sales_count_by_town_sub({},
                                                          "on_sale",
                                                          calc_date_from,
                                                          calc_date_to)
        
        calc_date_from, calc_date_to = \
            self.get_weekly_period( today - datetime.timedelta(days= 7) )

        ret_datas_tmp = self.calc_sales_count_by_town_sub(ret_datas_tmp,
                                                          "sold",
                                                          calc_date_from,
                                                          calc_date_to)
        
        ret_datas = []
        for pref_city_town, town_info in ret_datas_tmp.items():
            (town_info["pref"],town_info["city"],town_info["town"]) = \
                pref_city_town.split("\t")

            for calc_key in ["on_sale","sold"]:
                count_key = calc_key+"_count"
                price_key = calc_key+"_price"
                days_key  = calc_key+"_price"
                
                if not town_info[count_key]:
                    continue

                town_info[price_key] = \
                    town_info[price_key] / town_info[count_key]
                town_info[days_key] = \
                    town_info[days_key] / town_info[count_key]

            ret_datas.append(town_info)

        util_db = Db()
        util_db.save_tbl_rows("newbuild_sales_count_by_town",
                              ["pref","city","town","calc_date","calc_days",
                               "sold_count",   "sold_price",   "sold_days",
                               "on_sale_count","on_sale_price","on_sale_days"],
                              ret_datas)
        return ret_datas

    def calc_sales_count_by_town_sub(self,
                                     ret_datas_tmp,
                                     calc_key,
                                     calc_date_from,
                                     calc_date_to):
        
        suumo_service = SuumoService()
        org_bukkens = suumo_service.get_bukkens_by_check_date("新築戸建",
                                                              calc_date_from,
                                                              calc_date_to)
        # refer to https://qiita.com/acro5piano/items/e0a48905159e8a4911ab
        re_compile = re.compile("^([あ-んア-ン一-鿐]+)")

        for org_bukken in org_bukkens:
            if not org_bukken["pref"]:
                org_bukken["pref"] = "?"
            if not org_bukken["city"]:
                org_bukken["city"] = "?"

            town = org_bukken["address"]
            re_result = re_compile.search( town )
            if re_result:
                town = re_result.group(1)

            pref_city_town = "%s\t%s\t%s" % (org_bukken["pref"],
                                             org_bukken["city"],
                                             town)
            
            if not pref_city_town in ret_datas_tmp:
                ret_datas_tmp[pref_city_town] = {
                    "calc_date" : str(calc_date_to),
                    "calc_days" : 7,
                    "sold_count": 0,
                    "sold_price": 0,
                    "sold_days" : 0,
                    "on_sale_count":0,
                    "on_sale_price":0,
                    "on_sale_days" :0 }


            ret_datas_tmp[pref_city_town][calc_key+"_count"] += 1
            if org_bukken["price"]:
                ret_datas_tmp[pref_city_town][calc_key+"_price"] += org_bukken["price"]

            tmp_days = org_bukken["check_date"] - org_bukken["found_date"]
            ret_datas_tmp[pref_city_town][calc_key+"_days"] += tmp_days.days

        return ret_datas_tmp
