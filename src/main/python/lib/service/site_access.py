#!python
# -*- coding: utf-8 -*-

import appbase
import datetime
# refer to https://takahoyo.hatenablog.com/entry/2015/01/20/115031
import geoip2.database
import glob
import re
import tarfile

from service.googlemap import GoogleMapService
from util.db import Db


re_pat_log_line = \
    " ".join(['^([^ ]*) ([^ ]*) ([^ ]*) \[([^]]*)\] "([^ ]*)(?: *([^ ]*)',
              '*([^ ]*))?" ([^ ]*) ([^ ]*) "(.*?)" "(.*?)"'])
re_log_line = re.compile(re_pat_log_line)

# access_log 日時 用 正規表現 例:12/Jun/2020:04:27:27 +0900
re_pat_time = '^(\d+)/(\S+)/(\d+):(\d+):(\d+):(\d+)'
re_time = re.compile(re_pat_time)

# month str->int
month_def = {"Jan":1,"Feb":2,"Mar":3,"Apr": 4,"May": 5,"Jun":6,
             "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

logger = None
geo_ip_reader = None

class SiteAccessService(appbase.AppBase):
    
    def __init__(self):
        global logger
        logger = self.get_logger()

        app_conf = self.get_conf()
        global geo_ip_reader
        geo_ip_reader = geoip2.database.Reader(app_conf["common"]["geoip2_mmdb"])


    def save_addr_for_ips(self):
        logger.info("start")

        gmap_service = GoogleMapService()
        org_ips = self.load_client_ips_for_geocode()
        i = 0
        while len(org_ips) > 0 and i < 500:
            i += 1
            logger.info("%d %s %s %s" % (i,
                                         org_ips[0]["client_ip"],
                                         org_ips[0]["lng"],
                                         org_ips[0]["lat"] ) )
            
            new_ips = gmap_service.conv_lng_lat_to_addrs( org_ips )
            for new_ip in new_ips:
                self.save_addr_for_lng_lat(new_ip)
                
            org_ips = self.load_client_ips_for_geocode()

            

        
        
    def load_client_ips_for_geocode(self):
        sql = """
SELECT * from site_access
WHERE pref is null OR pref ='' OR
      city is null OR city =''
LIMIT 100
"""
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:
                try:
                    db_cur.execute(sql)
                except Exception as e:
                    logger.error(e)
                    logger.error(city)
                    
                    return []

                ret_data = []
                for tmp_row in db_cur.fetchall():
                    ret_data.append( dict( tmp_row ) )
                return ret_data
            
    def save_addr_for_lng_lat(self, lng_lat_addr):

        sql  = """
UPDATE site_access
SET pref=%s, city=%s, address_other=%s
WHERE lng=%s AND lat=%s
"""
        sql_args = (lng_lat_addr["pref"],
                    lng_lat_addr["city"],
                    lng_lat_addr["address_other"],
                    lng_lat_addr["lng"],
                    lng_lat_addr["lat"])
        
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:

                try:
                    db_cur.execute(sql,sql_args)
                except Exception as e:
                    logger.error(e)
                    logger.error(sql)
                    logger.error(str(lng_lat_addr))
                    return False
                
            db_conn.commit()
        return True


    def find_client_ip_from_logs(self):
        app_conf = self.get_conf()
        ret_data = {}
        
        for site in app_conf["site_log"]:
            if not site in ret_data:
                ret_data[site] = {}
                
            log_dir = app_conf["site_log"][site]
            logger.info( site+" "+log_dir )
            log_files = glob.glob(log_dir + '/*access_log.*.tar.gz')

            for log_file in sorted(log_files):
                logger.info( site+" "+log_file )
                tmp_ret_data = self.find_client_ip_from_log(log_file)
                ret_data[site].update( tmp_ret_data )

            ret_data[site] = list( ret_data[site].keys() )

        return ret_data
    

    def find_client_ip_from_log(self, log_file):
        ret_data = {}

        with tarfile.open(name=log_file, mode='r') as tar:
            for file_info in tar.getmembers():
                f = tar.extractfile(file_info)
                for log_line in f.readlines():
                    cols = self.parse_apache_log_line(log_line.decode())
                    if not cols:
                        continue
                    
                    # 200系 or 300系 means success.
                    if not cols["status"][0] in ["2","3"]:
                        continue
                    
                    client_ip = cols["host"]
                    
                    # 検出済のIPは、以降、2重には判定しない
                    if client_ip == "127.0.0.1" or client_ip in ret_data:
                        continue
                    
                    # print( client_ip , cols["resource"] )
                    ret_data[client_ip] = 1

        return ret_data

    # def calc_geo_ips(self, client_ips):
    #     geo_ip_oks, geo_ip_ngs = self.calc_geo_ips_by_maxiind(client_ips)

    #     gmap_service = GoogleMapService()
    #     cache_lnglat_addr = {}
        
    #     for geo_ip_ok in geo_ip_oks:
    #         lnglat = "\t".join([str(geo_ip_ok["longitude"]),
    #                             str(geo_ip_ok["latitude"]) ])
    #         if lnglat in cache_lnglat_addr:
    #             geo_ip_ok["address_components"] = cache_lnglat_addr[lnglat]
    #             continue
            
    #         geocoded = gmap_service.conv_lng_lat_to_addr(geo_ip_ok["longitude"],
    #                                                      geo_ip_ok["latitude"] )
    #         if not "address_components" in geocoded:
    #             continue

    #         cache_lnglat_addr[lnglat] = geocoded["address_components"]
    #         geo_ip_ok["address_components"] = geocoded["address_components"]
            
    #     return geo_ip_oks
    

    def calc_geo_ips_by_maxiind(self, client_ips):
        calc_ok = []
        calc_ng = []
        
        for client_ip in client_ips:
            geo_ip = None
            try:
                geo_ip = geo_ip_reader.city( client_ip )
            except Exception as e:
                logger.error(e)
                logger.error(client_ip)
                continue
            
            if not geo_ip or \
               not "en" in geo_ip.country.names:
                calc_ng.append(client_ip)
                continue

            if geo_ip.country.names['en'] != "Japan":
                continue
            
            if not geo_ip.location:
                calc_ng.append(client_ip)
                continue

            calc_ok.append({"client_ip" :client_ip,
                            "lat"       :geo_ip.location.latitude,
                            "lng"       :geo_ip.location.longitude })
        return calc_ok, calc_ng
        
        
    def save_tbl_rows(self, site, client_ips):
        rows = []
        for client_ip in client_ips:
            client_ip["site"] = site

        util_db = Db()
        util_db.save_tbl_rows("site_access",
                              ["site","client_ip","lng","lat"],
                              client_ips )

    def parse_apache_log_line(self,log_line):
        match_result = re_log_line.match(log_line)
        if match_result == None:
            logger.error( log_line )
            return None

        log_cols = {'host'    :match_result.group(1),
                    'ident'   :match_result.group(2),
                    'user'    :match_result.group(3),
                    'time'    :match_result.group(4),
                    'method'  :match_result.group(5),
                    'resource':match_result.group(6),
                    'proto'   :match_result.group(7),
                    'status'  :match_result.group(8),
                    'bytes'   :match_result.group(9),
                    'referer' :match_result.group(10),
                    'agent'   :match_result.group(11) }

        match_result = re_time.match(log_cols["time"] )
        if match_result == None:
            logger.error( log_line )
            return None

        month = month_def[match_result.group(2)]

        log_cols["time"] = datetime.datetime(int(match_result.group(3)),
                                             int(month),
                                             int(match_result.group(1)),
                                             int(match_result.group(4)),
                                             int(match_result.group(5)),
                                             int(match_result.group(6)))
        return log_cols
                    
