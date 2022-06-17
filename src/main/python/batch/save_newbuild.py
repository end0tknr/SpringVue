#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.newbuild import NewBuildService

def main():
    newbuild_service = NewBuildService()
    ret_datas = newbuild_service.sales_count_by_shop()
    print( ret_datas )

if __name__ == '__main__':
    main()


