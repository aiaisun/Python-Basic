# coding: utf-8

def getAuthor(table):
    authorEle   = table.select("tr")[0].select("td")[0]
    author_name = authorEle.select("div.authi a")[0].text
    tdTag       = table.select("tr")[0].select("td")[0]
    
    author_post_cnt     = tdTag.select("dl.pil dd")[0].text
    author_score        = tdTag.select("dl.pil dd")[1].text.replace(" 點","")
    author_diving_value = tdTag.select("dl.pil dd")[2].text.replace(" 米","")
    
    return {
        "author_name" : author_name,
        "author_post_cnt"     : int(author_post_cnt),
        "author_score"        : int(author_score),
        "author_diving_value" : int(author_diving_value)
    }

def getContent(table):
    trTag = table.select("tr")[1]
    if trTag.i: trTag.i.extract()
    return trTag.text

def getTime(table):
    return table.select("td")[1].select("div.authi em")[0].text.replace("發表於 ","").replace(" AM","")
