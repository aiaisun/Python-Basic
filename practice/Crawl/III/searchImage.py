import helpSearchGoogleImage

# 開瀏覽器搜尋圖片
google = 'https://www.google.com.tw/imghp?hl=zh-TW&tab=wi&ogbl'
keyword = "MAC"
scrollTimes = 2
imageUrls = helpSearchGoogleImage.searchImage(google, keyword, scrollTimes)

# 存圖
print("step 6: saving pcitures...")
for i in imageUrls:
    try:
        helpSearchGoogleImage.getImage(i, keyword)
    except:
        print("{} error.".format(imageUrls.index(i)))
print("step 6: all saved.")

print("all step done.")


