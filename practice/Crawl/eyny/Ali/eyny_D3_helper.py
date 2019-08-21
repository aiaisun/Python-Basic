# coding: utf-8

def getAuthorInfo(soup_article):


    divTable = soup_article.select("div#postlist > div")
    # 作者資訊
    author = soup_article.select("div.authi")[0].text.replace("\n","")
    author_post_cnt = divTable[0].select("dl.pil dd")[0].text
    author_score = divTable[0].select("dl.pil dd")[1].text.replace(" 點","")
    author_diving_value = divTable[0].select("dl.pil dd")[2].text.replace(" 米","")
    return {"author": author, 
            "author_post_cnt": author_post_cnt, 
            "author_score": author_score, 
            "author_diving_value": author_diving_value
           }

def getContent(soup_article):
    
    divTable = soup_article.select("div#postlist > div")
    content = divTable[0].select("tr td.t_f")[0].text.replace("\r\n","\n").replace("\n"," ")
    
    #貼文資訊     
    title = soup_article.select("div#postlist h1 a")[0].text + soup_article.select("div#postlist h1 a")[1].text
    time = divTable[0].select("div.pi em")[0].text.replace("發表於 ","")
    review = soup_article.select("div#postlist span.xi1")[0].text
    res_cnt = soup_article.select("div#postlist span.xi1")[1].text
    content = divTable[0].select("tr td.t_f")[0].text.replace("\r\n","\n").replace("\n"," ")
    
    return {"content": content, 
            "title": title, 
            "review": review, 
            "time": time,
            "res_cnt":res_cnt
           }


def replyInfo(divTable):
    
    reply_author = divTable.select("div.authi")[0].text.replace("\n","")
    if "發表於" in reply_author:
        reply_author = "該用戶已被刪除"
        reply_content = divTable.select("tr td.t_f")[0].text.replace("\r\n","\n").replace("\n"," ")
        reply_post_cnt = "-"
        reply_score = "-"
        reply_diving_value = "-"
        reply_time = divTable.select("div.authi")[0].text.replace("\n","").replace("發表於 ","").replace("|只看該作者","")
        
        data={
        "replyer"               : reply_author,
        "reply time"            : reply_time,
        "replyer's post"        : reply_post_cnt,
        "replyer's score"       : reply_score,
        "replyer's diving value": reply_diving_value,
        "reply content"         : reply_content           
        }
    else:

        reply_content = divTable.select("tr td.t_f")[0].text.replace("\r\n","\n").replace("\n"," ")
        reply_post_cnt = divTable.select("dl.pil dd")[0].text
        reply_score = divTable.select("dl.pil dd")[1].text.replace(" 點","")
        reply_diving_value = divTable.select("dl.pil dd")[2].text.replace(" 米","")
        reply_time = divTable.select("div.pi em")[0].text
        
        data={
        "replyer"               : reply_author,
        "reply time"            : reply_time,
        "replyer's post"        : reply_post_cnt,
        "replyer's score"       : reply_score,
        "replyer's diving value": reply_diving_value,
        "reply content"         : reply_content           
        }
 
    return data
