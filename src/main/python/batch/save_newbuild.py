#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.newbuild import NewBuildService

def main():
    newbuild_service = NewBuildService()
    newbuild_service.calc_save_sales_count_by_shop()
    newbuild_service.calc_save_sales_count_by_shop_city()
    newbuild_service.calc_save_sales_count_by_city()
    newbuild_service.calc_save_sales_count_by_town()

if __name__ == '__main__':
    main()


