#!python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )
from service.adatascientist     import DataScientistService
from service.kokusei_population import KokuseiPopulationService

def main():
    ds = DataScientistService()
    ds.calc_correlation_1()

if __name__ == '__main__':
    main()
