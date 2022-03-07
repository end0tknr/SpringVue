#!python
# -*- coding: utf-8 -*-

import openpyxl
import os
import tempfile
import urllib.request

# https://www.soumu.go.jp/denshijiti/code.html
master_src_url = "https://www.soumu.go.jp/main_content/000730858.xlsx"
master_xlsx = "000730858.xlsx"

class CityService():
    
    def __init__(self):
        pass

    def download_master(self):
        ret_data = []
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_xlsx_path =os.path.join(tmp_dir, master_xlsx)
        
            try:
                data = urllib.request.urlopen(master_src_url).read()

                with open(tmp_xlsx_path, mode="wb") as fh:
                    fh.write(data)

                wbook = openpyxl.load_workbook(tmp_xlsx_path)
                for sheetname in wbook.sheetnames:
                    tmp_ret_data = self.load_wsheet( wbook[sheetname] )

                    ret_data.extend( tmp_ret_data )
            except:
                print("fail",master_src_url)

            return ret_data
        

    def load_wsheet(self, wsheet):
        ret_data = []

        headers = []
        col_no = 1
        while col_no < wsheet.max_column :
            header = wsheet.cell(column=col_no, row=1).value
            if not header:
                col_no += 1
                continue
                
            headers.append( header.replace("\n","") )
            col_no += 1

        row_no = 2
        while row_no < wsheet.max_row :
            col_no = 1
            ret_row = {}
            for header in headers:
                ret_row[header] = wsheet.cell(column=col_no, row=row_no).value
                col_no += 1
                
            ret_data.append(ret_row)
            row_no += 1
            
        return ret_data
