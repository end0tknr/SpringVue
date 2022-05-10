#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.suumo import SuumoService

def main():
    suumo_service = SuumoService()
    
    result_list_urls = suumo_service.find_search_result_list_url()

    suumo_service.del_search_result_list_urls()

    for build_type, result_list_urls in result_list_urls.items():
        suumo_service.save_search_result_list_urls(build_type,
                                                   result_list_urls)

if __name__ == '__main__':
    main()


