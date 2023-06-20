import urllib.request
import time
import pandas as pd
import re
from PIL import Image
import gc
import matplotlib.pyplot as plt
import os
from multiprocessing import Pool
import multiprocessing

def image_crawler(url_and_cat_id, target_size=(224, 224)):
    # cat_id
    cat_id = url_and_cat_id.split('__')[0]
    # url 
    url = url_and_cat_id.split('__')[1]
    # prd_id 
    prd_id = url_and_cat_id.split('__')[2]

    try:                                   
        urllib.request.urlretrieve(url, f'./bungae_images_v2/{cat_id}/{prd_id}.jpg')

        # image 사이즈 줄이기 
        image_path = f'./bungae_images_v2/{cat_id}/{prd_id}.jpg'
        # image가 잘 열릴때만 열어서 다시 재저장
        try:
            plt.imread(image_path) # jpg 이미지가 열리는지 확인

            image = Image.open(image_path)
            image = image.resize(target_size)
            # Save the resized image
            image.save(image_path)

            print(f'{prd_id} image crawled')
        # image가 잘 열리지 않으면 삭제해주기
        except:
            os.remove(image_path)
            print('removed')
    except:
        print('does not exist')
        pass 
    
    return 

def image_crawler_mp(url_cat_id_list:list):
    
    pool = multiprocessing.Pool(3) # cpu 개수 -> 3
    pool.map(image_crawler, url_cat_id_list) 
    
    pool.close()
    pool.join()
    
    gc.collect()

    return 

if __name__ == '__main__':
    
    start_time = time.time()

    with open('./bungae_cat_url_prd_list.txt', 'r') as file: 
        data = file.read()
    url_cat_id_list = data.split(',') # 상품 list

    for idx in range(9): 
        image_crawler_mp(url_cat_id_list[idx::9])
        time.sleep(30)
    
    end_time = time.time()
    print('수행시간', end_time-start_time)

    gc.collect()