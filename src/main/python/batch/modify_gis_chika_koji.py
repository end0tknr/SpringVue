#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.gis_chika_koji import GisChikaKojiService

def main():
    chika_koji_service = GisChikaKojiService()
    chika_koji_service.modify_pref_cities()


if __name__ == '__main__':
    main()


