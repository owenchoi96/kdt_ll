import requests
from fake_useragent import UserAgent
import json
import time
import pandas as pd
from sbth import get_sbth
import re

def open_and_preprocess_df():
    df = pd.read_csv('./json_and_excel_files_merged.csv')
    df = df.fillna('')
    df['url'] = df['최종 URL'] # url 컬럼 이름 바꾸기
    del df['최종 URL']
    
    # -- cat3 기준 기타 빼야 됨 --
    # -- 그리고 reset index --
    index_list = list(df['cat3'][df['cat3'].str.contains('기타')].index)
    df = df.drop(index=index_list).copy()
    df = df.reset_index(drop=True).copy()
    
    # -- url 부분에 api 단어 추가 -- 
    df['url'] = df['url'].map(lambda x : re.sub('(.com\/search)', '.com/api/search', x))
    
    return df

def base_crawling_code(url:str, iq:str, spec:str, cat_id:int, page_num:int):
    """
    url, iq, spec 세개를 인자로 받아 크롤링을 하는 함수. 
    """
    sbth = get_sbth()
    ua = UserAgent(verify_ssl=False) 
    fake_ua = ua.random
    headers = {
        'user-agent' : fake_ua,
        'cache-control' : 'no-cache, no-store, must-revalidate',
        'sbth' : sbth,
        'referer' : 'https://search.shopping.naver.com/search/category',    
    }

    params = (
        ('sort','rel'),
        ('pagingIndex', page_num),
        ('productSet', 'total'), 
        ('pagingSize','40'),
        ('viewType','list'),
        ('iq', iq),
        ('spec', spec)
    )
        
    prd_list = list()
    res = requests.get(url, headers=headers, params=params)
    if (res.status_code == 200):
        results = res.json()
        results = results['shoppingResult']['products'] # products 키 값안에 상품 정보 들어있음. 
        
        for result in results:
            prd_id = result['id'] # id
            prd_name = result['productName'] # name
            prd_image_url = result['imageUrl'] # image_url
            prd_low_price = result['lowPrice'] # low_price

            prd_list.append([str(prd_id), prd_name, str(cat_id), prd_image_url, str(prd_low_price)]) 
            
    else:
        pass
    
    return prd_list

def get_NaverPrd(url:str, iq:str, spec:str, cat_id:int, page_count = 400):
    """
    cat_id -> 크롤링하고자 하는 category id
    page_count -> 크롤링하고자 하는 페이지 수 (400 pages by default)
    """
    prd_list = list()
    for page_num in range(1, page_count+1): # 400 페이지 가져오기 
        prd_list += base_crawling_code(url, iq, spec, int(cat_id), page_num)
        print('page %d done'%page_num)
        
        if page_num % 50 == 0:
            print('\n-- paused for 5 sec in case not to be blocked after crawling 50 pages --\n')
            time.sleep(5)
            
    print(f'-- category id {int(cat_id)} done --')
    print(f'-- 데이터 개수 : {len(prd_list)} --')
    
    # -- prd_list에서 데이터 프레임 만들기 --
    df = pd.DataFrame(prd_list, columns = ['id', 'name', 'cat_id', 'image_url', 'low_price'])
    
    # -- csv 파일로 내보내기 --
    # -- why? 혹시나 막힐 수도 있으니 미리미리 데이터 프레임으로 만들어 놓자 -- 
    df.to_csv(f'./cat_id_{int(cat_id)}_DF.csv', index=False)
    
    return

def run_all_process():
    df = open_and_preprocess_df()
    
    for idx in range(len(df)):    # 우선 3개만 
        url = df.iloc[idx]['url']
        iq = df.iloc[idx]['iq']
        spec = df.iloc[idx]['spec']
        cat_id = df.iloc[idx]['cat_id']
        
        get_NaverPrd(url, iq, spec, cat_id) # page_count는 default로 400 페이지
        
        # -- 블락을 대비하여 좀 길게 time.sleep() --
        print('\n-- paused for 2 min not to be blocked after crawling one category --\n')
        time.sleep(120)
        
    return

if __name__ == '__main__':
    run_all_process()
    

