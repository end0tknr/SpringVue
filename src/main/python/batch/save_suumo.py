#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.suumo import SuumoService

def main():
    suumo_service = SuumoService()
    result_list_urls = suumo_service.find_search_result_list_url()
    


if __name__ == '__main__':
    main()


