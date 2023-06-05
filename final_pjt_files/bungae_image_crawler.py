# -- image_url의 형태가 예상한것과 달라서 list를 이용한 multiprocessing이 어려울 것 같음 -- 
# -- 수정 필요 --
import urllib.request
import time
import pandas as pd

def crawl_images_and_put_in_folders(df):
    
    removed_prd_id_list = list()
    
    start = time.time()
    
    for idx in range(len(df)):
        url = df.loc[idx, 'image_url']
        cat_id = df.loc[idx, 'cat_id']
        prd_id = df.loc[idx, 'product_id']
        # -- 사라진 상품들이 있을 수 있기 때문에 try/except로 확인 필요 -- 
        try:                                   # -- 폴더명은 변경될 수 있습니다 --
            urllib.request.urlretrieve(url, f'./bungae_fashion_image/{cat_id}/{prd_id}_image.jpg')
            end = time.time()
            print(f'{prd_id} image crawled')
        except:
            removed_prd_id_list.append(prd_id)
            pass 
    
    end = time.time()
    print(f'----- time lapsed : {end-start} -----')
    print(f'------ 사라진 상품 갯수 : {len(removed_prd_id_list)} --------', )
    
    # -- 사라진 상품 product_id 리스트 --
    # -- 나중에 해당 상품들은 없애야할 것으로 보임
    with open('./bungae_removed_prd_id.txt', 'w+') as file: 
        file.write(','.join(removed_prd_id_list))
        
    return 

if __name__ == '__main__':
    # -- bungae_image_df를 먼저 불러옵니다 --
    bungae_image_df = pd.read_csv('./bungae_image_df.csv')
    
    crawl_images_and_put_in_folders(bungae_image_df)