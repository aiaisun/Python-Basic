# coding: utf-8

import eyny_D3_parser


url = "https://www.eyny.com/member.php?mod=logging&action=login"

hiddenParams = eyny_D3_parser.getHiddenParams(url)
print("Step1 取得參數 OK")


loginsess = eyny_D3_parser.login( hiddenParams["cookie"], hiddenParams["formhash"])
print("Step2 登入 OK")



articleList = eyny_D3_parser.crawlArticleList(loginsess)
print("step3 文章列表取得 OK")

article_list = []
for link in articleList[1:10]:
    try:
        articleInfo = eyny_D3_parser.getArticleData(loginsess,link)
        article_list.append(articleInfo)
        print(link, "done")
    except:
        traceback.print_exc()
        print(link, "fail")



eyny_D3_parser.saveFile(article_list, "20190820-1-D3-EVNY.xlsx")



