# coding: utf-8

import requests , time, random, traceback
from bs4 import BeautifulSoup as bs
import pandas as pd
import eyny_D3_helper




def getHiddenParams(url):

    res0 = requests.get(url)
    soup0 = bs(res0.text,"lxml")

    cookie = soup0.select("input[name='cookietime']")[0]["value"]
    formhash = soup0.select("input[name='formhash']")[0]["value"]

    return {"cookie": cookie, "formhash": formhash}


def login(cookie, formhash):    
   
    login_url = "https://www.eyny.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LZbj0&inajax=1"
    login_headers = {
        "Host"      : "www.eyny.com",
        "Origin"    : "https://www.eyny.com",
        "Referer"   : "https://www.eyny.com/member.php?mod=logging&action=login",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    }

    payload = {
        "formhash"            : formhash,
        "referer"             : "https://www.eyny.com/./",
        "loginfield"          : "username",
        "username"            : "7003un",
        "password"            : "0939771419",
        "questionid"          : "0",
        "answer"              : "",
        "cookietime"          : cookie,
        "g-recaptcha-response": "03AOLTBLTUd1qbWQ38a7xd157mbTo1CKjAR4-X9S3tZdgdNuhZ3pIlWJRhJYc_ozrF38X3DByrbdGjdVr0YnFtL9MOIITlVoKBwsPbsD8bzklK3c5-FBSg9mgJa3JOG19kVnXsyNmSSXl7y8Vt57bzNjtzNohp5pH1YNtdFuqlDOQtIEX4_b3hDvHMPt56bOdd1Xd85FyaLHlconYo4Aia6ZpUGkAr7T2fBSi7Ix8crMUllEqQ2MaIWIUOPxklULMunzIXR2zq8W2rnzdRuwbtEgLbfZqhIq8956uQg1En3xJobMS6RK_0cWGyIoMesNs8351fTSn1i_ZwN3ujwIotX5VymQGafR4GWWqgzFdQAL8PBheU8J0NFBvm6cCbXAdvPeFl0sBXyOjO"
    }

    sess = requests.session()
    res1 = sess.post(login_url, headers = login_headers, data = payload)
    
    return sess



def crawlArticleList(sess):

    base_url = "https://www.eyny.com/"
    headers={
        "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    }

    D3 = base_url+"forum-1710-1.html"

    resD3 = sess.get(D3, headers = headers)
    soupD3 = bs(resD3.text,"lxml")
    
    page_info = soupD3.select("div.pg a")

    page_link_list = [ base_url + ele["href"] for ele in page_info[1:10] ]
    page_link_list.insert(0,D3)

    all_page_article_links = []
    for page in page_link_list:

        headers={
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
        }

        respages = sess.get(page, headers = headers)
        soupD3page = bs(respages.text,"lxml")

        if page == "https://www.eyny.com/forum-1710-1.html":
            for ele in soupD3page.select("div#threadlist th.common a.xst")[3:]:
                all_page_article_links.append(base_url + ele["href"] )
        else:
            for ele in soupD3page.select("div#threadlist th.common a.xst"):
                all_page_article_links.append(base_url + ele["href"] )


    return all_page_article_links 




def getArticleData(sess,link):

    headers={
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
        }
    res_article = sess.get(link, headers = headers)
    soup_article = bs(res_article.text,"lxml")

    divTable = soup_article.select("div#postlist > div")

    
    
    reply_data_list = []
    for i in divTable[1:-1]:
        replyDetail = eyny_D3_helper.replyInfo(i)
        
        reply_data_list.append(replyDetail)
        
           
    
    author = eyny_D3_helper.getAuthorInfo(soup_article)
    content = eyny_D3_helper.getContent(soup_article)
    articleData ={
        "title"               : content["title"],
        "time"                : content["time"],
        "author"              : author["author"],
        "review"              : content["review"],
        "reply number"        : content["res_cnt"],
        "author post"         : author["author_post_cnt"],
        "author score"        : author["author_score"],
        "author diving value" : author["author_diving_value"],
        "Content"             : content["content"],
        "reply"               : reply_data_list

    }
    return articleData


def saveFile(dataList,name):

    df = pd.DataFrame(dataList)
    df = df[["title","time","reply number","review","Content","author","author post","author score","author diving value","reply"]]
    df.to_excel(name,index=False)
    print("Step4. 存檔完成")