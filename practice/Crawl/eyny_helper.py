# coding: utf-8

import requests
import traceback
import pandas as pd
from bs4 import BeautifulSoup as bs
import eyny_parser

def getHiddenParams(url):
    
    res0  = requests.get(url)
    soup0 = bs(res0.text,"lxml")

    cookietime = soup0.select("input[name='cookietime']")[0]["value"]
    formhash   = soup0.select("input[name='formhash']")[0]["value"]
    # print(formhash)
    
    
    return {"cookietime" : cookietime, "formhash" : formhash}


def login(formhash, cookietime):
    
    loginUrl = "https://www.eyny.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LIhj1&inajax=1"

    payload = {
        "formhash"            : formhash,
        "referer"             : "https://www.eyny.com/thread-12290829-1-GU7Y04C7.html",
        "loginfield"          : "username",
        "username"            : "7003un",
        "password"            : "0939771419",
        "questionid"          : "0",
        "answer"              : "",
        "cookietime"          : cookietime,
        "g-recaptcha-response": "03AOLTBLSQ9n63zcqqPQQA5FCEohXZtKD76G2DoV6_HNsggOVi4BBFl7lxBDZLlCL3kyXWYbAIiRBuXN6L9e_qk1c5-R1B4noiWkEwx_IrKRP8Oshlp5N-P_J0EoikEfTMlrRjjLy59ox7PRyxoYWR9UN5cRG_5BT7iSGeeSJagwB1YZ710EbM9rqJKDrMnDzMtv9q6aL7omX0sWCu07SNZO7r81kInV8DhD7F3AMdchIZ8Y6TH-hvRUIOHnVNWG4yDo0m1TvtyUwHnDuVjq-d6sGJfSUGouoOabss2InPrhp321m79N6RUGM"
    }

    loginHeaders = {
        "Host": "www.eyny.com",
        "Origin": "https://www.eyny.com",
        "Referer": "https://www.eyny.com/member.php?mod=logging&action=login",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    }

    sess = requests.session()
    res = sess.post(loginUrl , headers = loginHeaders , data = payload)
    # print(res.text)
    # print(res.cookies.get_dict())
    
    return sess



def crawlArticleList(sess):

    # Step 2
    ### 取得文章列表
    baseUrl = "https://www.eyny.com/"
    forum = "forum-1710-1.html"
    links = []

    headers = {
        "Host": "www.eyny.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    }
    res  = sess.get(baseUrl+forum , headers = headers)
    soup = bs(res.text , "lxml") 

    subLinks = [ baseUrl+ele["href"] for ele in soup.select("div#threadlist table[summary] th.new a.xst")]
    links += subLinks


    # links
    nextLinks = [baseUrl+a["href"] for a in soup.select("div.pg a")[1:10]]
    lastLink  = baseUrl+forum

    for nextLink in nextLinks:
        headers["Refer"] = lastLink

        res  = sess.get(nextLink , headers = headers)
        subSoup = bs(res.text , "lxml") 

        subLinks = [ baseUrl+ele["href"] for ele in subSoup.select("div#threadlist table[summary] th.common a.xst")]
        links += subLinks

        lastLink = nextLink
        
    return links


def crawlArticleDetail(sess,links):

    dataList = []
    for l in links:
        headers = {
        "Host": "www.eyny.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    }
              
        try:
    #     res2  = requests.get(l,headers=headers)
            res2  = sess.get(l,headers=headers)
            soup2 = bs(res2.text,"lxml")
            tableHeader = soup2.select("div#postlist > table")[0]

            pageview = tableHeader.select("td")[0].select("span")[1].text
            resp_cnt = tableHeader.select("td")[0].select("span")[4].text
            title    = tableHeader.select("td")[1].text.replace("[複製鏈接]","")

            tables = soup2.select("div#postlist > div > table")
            mainTable = tables[0]

            author   = eyny_parser.getAuthor(mainTable)
            content  = eyny_parser.getContent(mainTable)
            time     = eyny_parser.getTime(mainTable)

            data = {
                "title" : title,
                "time"  : time,
                "content" : content,
                "pageview": pageview,
                "resp_cnt": resp_cnt,
                "author_name"          : author["author_name"],
                "author_post_cnt"      : author["author_post_cnt"],
                "author_score"         : author["author_score"],
                "author_diving_value"  : author["author_diving_value"],
                "resp": []
            }

            for table in tables[1:]:
                respAuthor = eyny_parser.getAuthor(table)
                resp_data = {
                    "time"                : eyny_parser.getTime(table),
                    "content"             : eyny_parser.getContent(table),
                    "author_name"         : respAuthor["author_name"],
                    "author_post_cnt"     : respAuthor["author_post_cnt"],
                    "author_score"        : respAuthor["author_score"],
                    "author_diving_value" : respAuthor["author_diving_value"],
                }

                data["resp"].append(resp_data)


            dataList.append(data)

            ### 檢查是否文章有效
            print(data["title"])
            print("="*80)
        except:
            print("*"*80)
            traceback.print_exc()
            print("*"*80)
            
    return dataList


def saveFile(dataList,name):

    df = pd.DataFrame(dataList)
    df = df[["title","time","resp_cnt","pageview","content","author_name","author_post_cnt","author_score","author_diving_value","resp"]]
    df.to_excel(name,index=False)

