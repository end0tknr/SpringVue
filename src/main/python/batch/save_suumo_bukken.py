#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.suumo import SuumoService

def main():
    suumo_service = SuumoService()

    # 物件一覧のurl探索
    result_list_urls = suumo_service.find_search_result_list_url()

    # 物件一覧の旧url 削除
    suumo_service.del_search_result_list_urls()

    # 物件一覧の新url 登録
    for build_type, result_list_urls in result_list_urls.items():
        suumo_service.save_search_result_list_urls(build_type,
                                                   result_list_urls)

    # 物件一覧の新url 再? load
    result_list_urls = suumo_service.load_search_result_list_urls()

    # 各物件情報の取得と保存
    for result_list_tmp in result_list_urls:
        build_type      = result_list_tmp[0]
        result_list_url = result_list_tmp[1]
        bukken_infos = suumo_service.parse_bukken_infos(result_list_url)

        suumo_service.save_bukken_infos(build_type,bukken_infos)


if __name__ == '__main__':
    main()


