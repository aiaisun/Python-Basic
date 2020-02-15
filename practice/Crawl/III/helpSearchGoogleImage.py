from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib
import os
import requests
from bs4 import BeautifulSoup
from time import sleep

# 存圖片
def getImage(url, keyword):
    res = requests.get(url)
    if not os.path.isdir(keyword):
        os.mkdir(keyword)
    
    with open(f'{keyword}/{os.path.basename(url)}.jpg','wb') as f:
        f.write(res.content)

# open browser
# search keyword's image
def searchImage(url, keyword, scrollTimes):
    #開瀏覽器
    chromeDriver = './chromedriver' # chromedriver檔案放的位置
    driver = webdriver.Chrome(chromeDriver)
    driver.maximize_window()
    driver.get(url)
    print("step 1: open browser done.")
    
    #輸入關鍵字
    driver.find_element_by_name("q").send_keys(keyword)
    driver.find_element_by_name("q").send_keys("\ue007")
    print("step 2: insert keyword {} done.".format(keyword))
    
    #捲動網頁
    currentUrl = driver.current_url
    imageUrls = []
    for i in range(1, scrollTimes):
        driver.execute_script("window.scrollTo(0,{})".format(i*2000))
        sleep(5)
    print("step 3: Scroll {} times done.".format(scrollTimes-1))
    
    #找到所有圖片的url
    allImageTag = driver.find_elements_by_css_selector("img")
    # allPic
    for picture in allImageTag:
        if picture.get_attribute('src'):
            imageUrls.append(picture.get_attribute('src'))

    print("step 4: get all url done. Quantity: {}.".format(len(imageUrls)))
    
    # 爬前20張
    resp = requests.get(currentUrl)
    soup = BeautifulSoup(resp.text, 'lxml')
    soup.select("img")
    imgList = [ ele["src"] for ele in soup.select("img") ]
    for ele in soup.select("img"):
        getImage(ele["src"], keyword)
        
    print("step 5: saved first 20 pictures done.")
    
    return imageUrls