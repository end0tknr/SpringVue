#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.mlit_realestateshop import MlitRealEstateShopService

def main():
    real_estate_shop_service = MlitRealEstateShopService()

    shops = real_estate_shop_service.find_licence_def("第005707号")
    print( shops )
    

if __name__ == '__main__':
    main()
