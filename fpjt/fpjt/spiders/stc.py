import requests
import pandas as pd
import os
import datetime

print(f'\n\n########## 시   작 ##########\n\n')

url_stc = 'https://kind.krx.co.kr/corpgeneral/corpList.do'


params_stc = {
    'method':'download',
    'pageIndex':1,
    'currentPageSize':3000,
    'comAbbrvTmp':'',
    'beginIndex':'',
    'orderMode':3,
    'orderStat':'D',
    'isurCd':'',
    'replsuSrtCd':'',
    'searchType':'',
    'marketType':'',
    'searchType':13,
    'industry':'',
    'fiscalYearEnc':'all',
    'comAbbrvTmp':'',
    'location':'all'
}    

headers ={
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Whale/3.20.182.14 Safari/537.36'
}

rs_stc = requests.post(url_stc, data=params_stc, headers=headers)

if rs_stc.status_code != 200:
    print(f'\n☞ status_code Err :  {rs_stc.status_code}')
else:
    print(f'\n☞ successful requests & status_stockCode  :  {rs_stc.status_code}')
    df_code = pd.read_html(rs_stc.text, converters={'종목코드': str})[0]
    df_code['종목코드'] = '"'+ df_code['종목코드'] + '"' #종목코드 숫자앞 0이 유지되면서 to_csv()로 출력되도록 한 코딩임
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name = f'stockCode_{stamp}.csv'
    file_path = os.path.join(os.getcwd(), 'fhs', file_name)
    df_code.to_csv(file_path, index=False)
        #DataFrame의 인덱스를 csv파일에 포함시키지 않으려고 False로 설정
    print(f'\n\n########## 종   료 ##########\n\n')