#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.gis_youto_chiiki import GisYoutoChiikiService

def main():
    youto_chiiki_service = GisYoutoChiikiService()
    org_cities = youto_chiiki_service.modify_seirei_city_names()
    print( org_cities )

if __name__ == '__main__':
    main()


