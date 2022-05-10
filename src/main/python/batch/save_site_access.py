#!python3
# -*- coding: utf-8 -*-

import getopt
import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '../lib') )

from service.site_access import SiteAccessService
from service.googlemap   import GoogleMapService

def main():
    site_access_service = SiteAccessService()
    
    # site_client_ips = site_access_service.find_client_ip_from_logs()

    # for site in site_client_ips:
    #     clinet_ips = site_client_ips[site]
    #     ip_lnglat_oks,ip_lnglat_ngs = \
    #         site_access_service.calc_geo_ips_by_maxiind(clinet_ips)

    #     site_access_service.save_tbl_rows(site, ip_lnglat_oks)

    site_access_service.save_addr_for_ips()
    
    # gmap_service = GoogleMapService()
    # org_ips = site_access_service.load_client_ips_for_geocode()
    # new_ips = gmap_service.conv_lng_lat_to_addrs( org_ips )
    # for new_ip in new_ips:
    #     site_access_service.save_addr_for_lng_lat(new_ip)

        
if __name__ == '__main__':
    main()
    
