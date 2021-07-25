# 7old
# search engine
#  crawl engine

from table import savedb
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import re


def findurls(s):
    return re.findall(r'href=[\'"]?([^\'" >]+)', s)


def gettitle(s):
    result = re.search(r'<title>(.*?)</title>', s)
    if result is not None:
        return result.group(1)[:100]
    else:
        return "No title provided"


def getdesc(s):
    result = re.search(
        r'<meta[^>]*name=[\"|\']description[\"|\'][^>]*content=[\"]([^\"]*)[\"][^>]*>', s)
    if result is not None:
        return result.group(1)[:250]
    else:
        return "No description provided"


def docrawl(query, recrawl=True):
    if len(query) > 100:
        return
    try:
        # try to solve some common problems that cannot be handled by
        # the urllib
        query = "https://" + query[2:] if query.startswith("//") else query
        query = query.replace("/./", "/")
        query = re.sub(r'(?<!:)\/\/+', "/", query)
        # request, if this fails, it jumps to except
        req = Request(query, headers={"User-Agent": "Mozilla/5.0"})
        res = urlopen(req)
        str = res.read().decode("utf8")
        res.close()
        print("[!] Success fetching ->", query)
    except Exception as e:
        print("[!] Error fetching a submitted website (", query, ") -> ", e)
        # since docrawl() algorithm is pretty simple and sometimes
        # fails (i don't really want to use external libraries)
        # it tries with some combinations that may be helpful
        # /!\ you can uncomment the if recrawl: line, but that
        # may cause infinite (or nearly) loops
        if recrawl:
            if not query.endswith("/"):
                docrawl(query + "/")
            if '..' in query:
                docrawl(urljoin(query, '.'))
    else:
        # the website has been reached (its contents too),
        # add it to the db then
        savedb((gettitle(str), query, getdesc(str)))

        # debug purposes, you may comment this
        # print("Title ->", gettitle(str))
        # print("Desc ->", getdesc(str))
        # if recrawl: print(query, "->", ', '.join(findurls(str)))

        # this crawls found urls inside the website itself
        # with a limit of 40 urls (you may change this limit)
        # False avoids recursive (and usually infinite)
        # crawling of found pages
        if recrawl:
            limit = 0
            urls = findurls(str)
            for i in urls:
                if limit <= 40 and i != query:
                    if i.startswith("//") or i.startswith("https://") or i.startswith("http://"):
                        docrawl(i, False)
                    # elif query.endswith("/") or i.endswith("/"):
                    #     if query.endswith("/") and i.endswith("/"):
                    #         if (query[:(len(query)-1)] + i) != i:
                    #             docrawl((query[:(len(query)-1)] + i), False)
                    #     else:
                    #         if (query + i) != i:
                    #             docrawl((query + i), False)
                    elif i.startswith('/'):
                        resolved = re.search(
                            r'^(http|https):\/\/(.*?)\/', query + "/").group(0) + i
                        if resolved != query:
                            docrawl(resolved, False)
                    else:
                        docrawl((query + "/" + i), False)
                    limit += 1
