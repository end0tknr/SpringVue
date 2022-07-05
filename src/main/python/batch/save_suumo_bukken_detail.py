#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.suumo import SuumoService

def main():
    suumo_service = SuumoService()
#    suumo_service.save_bukken_details( '新築戸建',"shop is null" )
    suumo_service.save_bukken_details( '中古戸建',"shop is null" )
#    suumo_service.save_bukken_details( '新築戸建',"" )
#    suumo_service.save_bukken_details( '中古戸建',"" )

if __name__ == '__main__':
    main()


