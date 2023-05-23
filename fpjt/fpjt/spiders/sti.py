import pandas as pd
import scrapy
import os
import glob
from bs4 import BeautifulSoup
#from items import FpjtItem

class StiSpider(scrapy.Spider):
    name = "sti"
    
    def start_requests(self):
        file_path = os.path.join(os.getcwd(), 'fhs', 'stockCodeTest.csv')
        stcd = pd.read_csv(file_path)
        stcd['종목코드'] = stcd['종목코드'].str.strip('""')
        for code in stcd['종목코드']:
            url=f'https://navercomp.wisereport.co.kr/v2/company/ajax/cF1001.aspx?cmp_cd={code}'
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Whale/3.20.182.14 Safari/537.36'
            }
            scr = scrapy.Request(url, callback=self.parse, meta=params_sti, headers=headers)
            yield scr
    def parse(self, rs):
        sp = BeautifulSoup(rs.text, 'html.parser')
        print(sp)
            
        
        
            
    

