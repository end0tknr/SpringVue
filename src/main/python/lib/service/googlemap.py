#!python
# -*- coding: utf-8 -*-

import appbase
import json
import re
import urllib.parse
import urllib.request

geocode_api = "https://maps.google.com/maps/api/geocode/json"
logger = appbase.AppBase.get_logger()


class GoogleMapService(appbase.AppBase):
    
    def __init__(self):
        pass

    def save_latlan_to_db(self, new_data):
        dbh = self.db_connect()
        cur = dbh.cursor()

        atri_keys = []
        atri_args = []
        atri_vals = []
        for atri_key in ["lng","lat","mesh_code","address"]:
            if atri_key in new_data:
                atri_keys.append(atri_key)
                atri_args.append("%s")
                atri_vals.append(new_data[atri_key])
                
        sql = "INSERT INTO gis_latlng_addr (%s) VALUES (%s)" \
            % (",".join(atri_keys), ",".join(atri_args))

        cur.execute(sql,atri_vals)
        dbh.commit()
        return True
    
    def get_latlan_from_db_by_mesh_code(self, mesh_code):
        ret_rows = []
        db_conn = self.db_connect()
        cur = self.db_cursor(db_conn)
        sql = "SELECT * FROM gis_latlng_addr WHERE mesh_code=%s"
        cur.execute(sql, [str(mesh_code)])
        for row in cur.fetchall():
            ret_rows.append( dict(row) )
                
        return ret_rows

    #refer to https://www.pasco.co.jp/recommend/word/word012/
    def conv_gis_mesh_code_to_lat_lng(self,gis_mesh_code):
        lat_lng = self.get_latlan_from_db_by_mesh_code(mesh_code)
        if lat_lng:
            return lat_lng

        parsed_mesh_code = \
        re.compile('^(\d\d)(\d\d)(\d)?(\d)?(\d)?(\d)?$').findall(gis_mesh_code)
        
        if len( parsed_mesh_code ) == 0:
            return None

        # 1次meshの緯度/経度化 (約6400km2)
        lat_lng['lat'] = int( parsed_mesh_code[0][0] ) / 1.5 #緯度
        lat_lng['lng'] = int( parsed_mesh_code[0][1] ) + 100 #経度

        # 2次meshの桁がない場合、ココまで
        if len(parsed_mesh_code[0][2])==0 or len(parsed_mesh_code[0][3]) ==0:
            self.save_latlan_addr_to_db(lat_lng)
            return lat_lng
        
        # 2次meshの緯度/経度化 (約100km2)
        lat_lng['lat'] += int(parsed_mesh_code[0][2])/8 * 2/3
        lat_lng['lng'] += int(parsed_mesh_code[0][3])/8

        # 3次meshの桁がない場合、ココまで
        if len(parsed_mesh_code[0][4])==0 or len(parsed_mesh_code[0][5]) ==0:
            self.save_latlan_addr_to_db(lat_lng)
            return lat_lng
        
        # 3次meshの緯度/経度化 (約1km2)
        lat_lng['lat'] += int(parsed_mesh_code[0][4])/80 * 2/3
        lat_lng['lng'] += int(parsed_mesh_code[0][5])/80
        self.save_latlan_addr_to_db(lat_lng)
        return lat_lng
    
        
    #例 https://maps.google.com/maps/api/geocode/json?address=渋谷&key=ないしょ
    def conv_addr_to_latlng_by_api(self,address_str):
        conf = self.get_conf()
        
        req_params = {}
        req_params["key"]      = conf["common"]["google_map_api_key"]
        req_params["language"] = "ja"
        req_params["address"]  = address_str
        req_params_str = urllib.parse.urlencode(req_params)

        req_url = geocode_api +"?"+ req_params_str
        print( req_url )
        req = urllib.request.Request(req_url)
        try:
            res = urllib.request.urlopen(req)
        except:
            return None

        content_str = res.read()
        res.close()
    
        content = json.loads(content_str)
        if content['status'] != "OK":
            return None

        ret_data = content["results"][0]["geometry"]["location"]
        tmp_address = content["results"][0]["formatted_address"]
        ret_data.update( self.parse_formatted_address(tmp_address) )
        
        return ret_data
        
    def conv_lat_lng_to_addr_by_api(self,lat,lng): # lat:緯度, lng:経度
        conf = self.get_conf()
        
        req_params = {}
        req_params["key"]      = conf["common"]["google_map_api_key"]
        req_params["language"] = "ja"
        req_params["latlng"] = str(lat)+","+str(lng)

        req_params_str = []
        for atri_key, atri_val in req_params.items():
            req_params_str.append( atri_key+"="+ atri_val)

            
        req_url = geocode_api +"?"+ "&".join(req_params_str)
        req = urllib.request.Request(req_url)
        try:
            res = urllib.request.urlopen(req)
        except:
            return None

        content_str = res.read()
        res.close()
    
        content = json.loads(content_str)
        if content['status'] != "OK":
            return None

        ret_data = content["results"][0]["geometry"]["location"]
        tmp_address = content["results"][0]["formatted_address"]
        ret_data.update( self.parse_formatted_address(tmp_address) )

        return ret_data


    def parse_formatted_address(self,formatted_address):
        # ex. 日本、〒373-0073 群馬県太田市緑町４０８
        re_result = \
            re.compile('〒(\d\d\d-\d\d\d\d) (.+)$').search(formatted_address)
        if re_result:
            return {"zip_code": re_result.group(1),
                    "address" : re_result.group(2) }

        # ex. 2222+22 日本、埼玉県小鹿野町
        re_result = re.compile('日本、(.+)$').search(formatted_address)
        if re_result:
            return {"address" : re_result.group(1)}

        return {"address" : formatted_address}
