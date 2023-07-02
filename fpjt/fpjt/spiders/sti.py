import pandas as pd
import scrapy
import os
import glob
from bs4 import BeautifulSoup
from fpjt.items import FpjtItem

class StiSpider(scrapy.Spider):
    name = "sti"
    
    def start_requests(self):
        file_path = os.path.join(os.getcwd(), 'fhs')
        print(f'\n★★★★★★★★★★★★★경로확인_fhs★★★★★★★:  {file_path}\n')
        file_list = glob.glob(os.path.join(file_path, 'stockCode_*.csv'))
        file_latest = max(file_list, key = os.path.getctime)
        stcd = pd.read_csv(file_latest)
        stcd['종목코드'] = stcd['종목코드'].str.strip('""')
        for code in stcd['종목코드']:
            url=f'https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={code}'
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
            }
            scr = scrapy.Request(url, callback=self.parse, meta={'code':code}, headers=headers)
            yield scr
            
                            
    def parse(self, rs):
        code = rs.meta['code']
        item = FpjtItem() 
        item['종목명'] = rs.css('.name::text').get()
        item['종목코드'] = code
        item['종목코드'] = '"'+item['종목코드']+'"'
        item['시장구분'] = rs.css('dl dt:nth-child(3)::text').get().split(':')[0].strip()
        item['업종구분'] = rs.css('dl dt:nth-child(3)::text').get().split(':')[1].strip()
        item['상세구분'] = rs.css('dl dt:nth-child(4)::text').get().split(':')[1].strip()
        item['투자의견'] = rs.css('#pointerVal::text').get()
        item['투자의견'] = float(''.join(filter(str.isdigit, item['투자의견'] or ''))) if item['투자의견'] else None  
        
        item['현재가'] = rs.css('#cTB11 > tbody > tr:nth-child(1) > td > strong::text').get()
        item['현재가'] = float(''.join(filter(str.isdigit, item['현재가'] or ''))) if item['현재가'] else None
        item['PER'] = rs.css('#wrapper > div.fund.fl_le > table > tbody > tr:nth-child(1) > td:nth-child(2)::text').get()
        item['PER'] = ''.join(filter(str.isdigit, item['PER']))
        item['PER'] = float(item['PER']) /100 if item['PER'] else None
        item['PBR'] = rs.css('#wrapper > div.fund.fl_le > table > tbody > tr:nth-child(2) > td:nth-child(2)::text').get()
        item['PBR'] = ''.join(filter(str.isdigit, item['PBR']))
        item['PBR'] = float(item['PBR']) /100 if item['PBR'] else None
        item['EV_EBITDA'] = rs.css('#wrapper > div.fund.fl_le > table > tbody > tr:nth-child(4) > td:nth-child(2)::text').get()
        item['EV_EBITDA'] = float(''.join(filter(str.isdigit, item['EV_EBITDA'] or '')))/100 if item['EV_EBITDA'] else None  
        

#        yield item
        # 크롤링 추가
        
        naver_url = f'https://finance.naver.com/item/main.naver?code={code}'
        scr_naver = scrapy.Request(naver_url, callback=self.parse_naver, meta={'item': item})
        yield scr_naver

    def parse_naver(self, rs):
        item = rs.meta['item']    
        item['매출액'] = rs.css('#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(1) > td:nth-child(4)::text').get()
        item['매출액'] = ''.join(filter(str.isdigit, item['매출액']))
        item['매출액'] = float(item['매출액']) if item['매출액'] else None
        
        np_1 = '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(3) > td:nth-child(4)::text'
        np_2 = '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(3) > td:nth-child(4) > em::text' # CSS셀렉터가 #content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(3) > td:nth-child(4) > em 인 경우까지 포함
        item['순이익'] = rs.css(np_1).get(default='').strip() or rs.css(np_2).get(default='').strip()
        
        npr_1 = '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(5) > td:nth-child(4)::text'                      
        npr_2 = '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(5) > td:nth-child(4) > em::text'
        item['순이익율'] = rs.css(npr_1).get(default='').strip() or rs.css(npr_2).get(default='').strip()     
                                
        r_1 = '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(6) > td:nth-child(4)::text'
        r_2 = '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(6) > td:nth-child(4) > em::text'                       
        item['ROE'] = rs.css(r_1).get(default='').strip() or rs.css(r_2).get(default='').strip()    
        item['ROE'] = float(''.join(filter(str.isdigit, item['ROE'] or '')))/100 if item['ROE'] else None  
     
                                        
        item['배당수익율'] = rs.css('#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(15) > td:nth-child(4)::text').get()
        item['배당수익율'] = ''.join(filter(str.isdigit, item['배당수익율']))
        item['배당수익율'] = float(item['배당수익율']) /100 if item['배당수익율'] else None
        item['부채비율'] = rs.css('#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(7) > td:nth-child(4)::text').get()
        item['부채비율'] = float(''.join(filter(str.isdigit, item['부채비율'] or '')))/100 if item['부채비율'] else None  
            
        
  
        yield item            
 

##################

# import pandas as pd
# import scrapy
# import os
# import glob
# from bs4 import BeautifulSoup
# from fpjt.items import FpjtItem

# class StiSpider(scrapy.Spider):
#     name = "sti"
#     df_sti = None  # 클래스 멤버 변수로 선언

#     def start_requests(self):
#         file_path = os.path.join(os.getcwd(), 'fhs')
#         print(f'\n★★★★★★★★★★★★★경로확인_fhs★★★★★★★:  {file_path}\n')
#         file_list = glob.glob(os.path.join(file_path, 'stockCode_*.csv'))
#         file_latest = max(file_list, key=os.path.getctime)
#         self.df_sti = pd.read_csv(file_latest)

#         stcd = self.df_sti['종목코드'].str.strip('""')
#         for code in stcd:
#             url = f'https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={code}'
#             headers = {
#                 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
#             }
#             scr = scrapy.Request(url, callback=self.parse, meta={'code': code}, headers=headers)
#             yield scr

#     def parse(self, rs):
#         code = rs.meta['code']
#         item = FpjtItem()
#         item['종목명'] = rs.css('.name::text').get()
#         item['종목코드'] = code
#         item['종목코드'] = '"' + item['종목코드'] + '"'
#         item['시장구분'] = rs.css('dl dt:nth-child(3)::text').get().split(':')[0].strip()
#         item['업종구분'] = rs.css('dl dt:nth-child(3)::text').get().split(':')[1].strip()
#         item['상세구분'] = rs.css('dl dt:nth-child(4)::text').get().split(':')[1].strip()
#         item['투자의견'] = rs.css('#pointerVal::text').get()
#         item['투자의견'] = ''.join(filter(str.isdigit, item['투자의견']))
#         item['투자의견'] = float(item['투자의견']) if item['투자의견'] else None
#         item['현재가'] = rs.css('#cTB11 > tbody > tr:nth-child(1) > td > strong::text').get()
#         item['현재가'] = float(''.join(filter(str.isdigit, item['현재가'] or ''))) if item['현재가'] else None
#         item['PER'] = rs.css('#wrapper > div.fund.fl_le > table > tbody > tr:nth-child(1) > td:nth-child(2)::text').get()
#         item['PER'] = ''.join(filter(str.isdigit, item['PER']))
#         item['PER'] = float(item['PER']) / 100 if item['PER'] else None
#         item['PBR'] = rs.css('#wrapper > div.fund.fl_le > table > tbody > tr:nth-child(2) > td:nth-child(2)::text').get()
#         item['PBR'] = ''.join(filter(str.isdigit, item['PBR']))
#         item['PBR'] = float(item['PBR']) / 100 if item['PBR'] else None
#         item['EV_EBITDA'] = rs.css('#wrapper > div.fund.fl_le > table > tbody > tr:nth-child(4) > td:nth-child(2)::text').get()
#         item['EV_EBITDA'] = ''.join(filter(str.isdigit, item['EV_EBITDA']))
#         item['EV_EBITDA'] = float(item['EV_EBITDA']) / 100 if item['EV_EBITDA'] else None

#         # 크롤링 추가

#         naver_url = f'https://finance.naver.com/item/main.naver?code={code}'
#         scr_naver = scrapy.Request(naver_url, callback=self.parse_naver, meta={'item': item})
#         yield scr_naver

#     def parse_naver(self, rs):
#         item = rs.meta['item']

#         # 필터링 조건 계산
#         condi_1 = (self.df_sti['PER'] <= 20) & (self.df_sti['PBR'] <= 2) & (self.df_sti['배당수익율'] >= 2) & (self.df_sti['EV_EBITDA'] < 5) & (self.df_sti['부채비율'] <= 100) & (self.df_sti['ROE'] >= 10)
#         condi_2 = self.df_sti['투자의견'].notna()
#         condi_3 = condi_1 | condi_2

#         item['매출액'] = rs.css('#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(1) > td:nth-child(4)::text').get()
#         item['매출액'] = ''.join(filter(str.isdigit, item['매출액']))
#         item['매출액'] = float(item['매출액']) if item['매출액'] else None

#         np_1 = '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(3) > td:nth-child(4)::text'
#         np_2 = '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(3) > td:nth-child(4) > em::text' # CSS셀렉터가 #content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(3) > td:nth-child(4) > em 인 경우까지 포함
#         item['순이익'] = rs.css(np_1).get(default='').strip() or rs.css(np_2).get(default='').strip()

#         npr_1 = '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(5) > td:nth-child(4)::text'
#         npr_2 = '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(5) > td:nth-child(4) > em::text'
#         item['순이익율'] = rs.css(npr_1).get(default='').strip() or rs.css(npr_2).get(default='').strip()

#         r_1 = '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(6) > td:nth-child(4)::text'
#         r_2 = '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(6) > td:nth-child(4) > em::text'
#         item['ROE'] = rs.css(r_1).get(default='').strip() or rs.css(r_2).get(default='').strip()
#         item['ROE'] = ''.join(filter(str.isdigit, item['ROE']))
#         item['ROE'] = float(item['ROE']) / 100 if item['ROE'] else None

#         item['배당수익율'] = rs.css('#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(15) > td:nth-child(4)::text').get()
#         item['배당수익율'] = ''.join(filter(str.isdigit, item['배당수익율']))
#         item['배당수익율'] = float(item['배당수익율']) / 100 if item['배당수익율'] else None
#         item['부채비율'] = rs.css('#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(7) > td:nth-child(4)::text').get()
#         item['부채비율'] = float(''.join(filter(str.isdigit, item['부채비율'] or ''))) / 100 if item['부채비율'] else None

#         yield item
