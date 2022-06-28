#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.sumstock import SumStockService

def main():
    sumstock_service = SumStockService()
    # sumstock_service.calc_save_sales_count_by_shop()
    # sumstock_service.calc_save_sales_count_by_shop_city()
    # sumstock_service.calc_save_sales_count_by_city()
    # sumstock_service.calc_save_sales_count_by_town()
    sumstock_service.calc_save_sales_count_by_price()


if __name__ == '__main__':
    main()


