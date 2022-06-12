#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.suumo import SuumoService

def main():
    suumo_service = SuumoService()
    suumo_service.save_bukken_details()

if __name__ == '__main__':
    main()


