#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.suumo import SuumoService

def main():
    suumo_service = SuumoService()
    result_list_urls = suumo_service.load_search_result_list_urls()

    for result_list_tmp in result_list_urls:
        build_type      = result_list_tmp[0]
        result_list_url = result_list_tmp[1]
        bukken_infos = suumo_service.parse_bukken_infos(result_list_url)

        suumo_service.save_bukken_infos(build_type,bukken_infos)

if __name__ == '__main__':
    main()


