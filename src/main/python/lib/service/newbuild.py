#!python
# -*- coding: utf-8 -*-

from service.suumo import SuumoService
from util.db import Db
import appbase
import datetime

logger = None

class NewBuildService(appbase.AppBase):

    def __init__(self):
        global logger
        logger = self.get_logger()

    def sales_count_by_shop_sub(self,
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
        
    def sales_count_by_shop(self):
        logger.info("start")
        
        today = datetime.datetime.today().date()
        calc_date_from, calc_date_to = self.get_weekly_period(today)

        ret_datas_tmp = self.sales_count_by_shop_sub({},
                                                     "on_sale",
                                                     calc_date_from,
                                                     calc_date_to)
        
        calc_date_from, calc_date_to = \
            self.get_weekly_period( today - datetime.timedelta(days= 7) )

        ret_datas_tmp = self.sales_count_by_shop_sub(ret_datas_tmp,
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

            
    def get_weekly_period(self,today):
        weekday = today.weekday() # 0=Mon ... 6=Sun
        calc_date_from = today - datetime.timedelta(days= weekday  ) # Mon
        calc_date_to   = today + datetime.timedelta(days= 6-weekday) # Sun
        return calc_date_from, calc_date_to
