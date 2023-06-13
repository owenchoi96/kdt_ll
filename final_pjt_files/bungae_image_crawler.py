# -- image_url의 형태가 예상한것과 달라서 list를 이용한 multiprocessing이 어려울 것 같음 -- 
import urllib.request
import time
import pandas as pd
import re
from PIL import Image
import gc
from multiprocessing import Pool
import multiprocessing

def crawl_images_and_put_in_folders(url_and_cat_id, target_size=(224, 224)):
    # cat_id
    cat_id = url_and_cat_id.split('__')[-1]

    # url 
    url = url_and_cat_id.split('__')[0]

    # prd_id
    prd_id = re.findall(r'\b\/\w+\_', url_and_cat_id)[-1]
    prd_id = prd_id.replace('/', '').replace('_', '')

    removed_prd_id = None
    try:                                   
        urllib.request.urlretrieve(url, f'./bungae_fashion_image/{cat_id}/{prd_id}_image.jpg')

        # image 사이즈 줄이기 
        image_path = f'./bungae_fashion_image/{cat_id}/{prd_id}_image.jpg'
        image = Image.open(image_path)
        image = image.resize(target_size)
        # Save the resized image
        image.save(image_path)

        print(f'{prd_id} image crawled')
    except:
        pass 
    
    return 

def url_cat_id_mp(url_cat_id_list:list):
    
    pool = multiprocessing.Pool(4) # cpu 개수 -> 4
    pool.map(crawl_images_and_put_in_folders, url_cat_id_list) 
    
    pool.close()
    pool.join()
    
    gc.collect()

    return 

if __name__ == '__main__':
    
    start_time = time.time()

    with open('./bungae_url_cat_id_list.txt', 'r') as file: 
        data = file.read()
    url_cat_id_list = data.split(',') # 상품 list

    for idx in range(9): # 분할해서 데이터 프레임으로 만들기 
        url_cat_id_mp(url_cat_id_list[idx::9])
        time.sleep(30)
    
    end_time = time.time()
    print('수행시간', end_time-start_time)

    gc.collect()