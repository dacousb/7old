# 7old
# search engine
#  crawl engine

from table import savedb
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def docrawl(query, recrawl=True):
    if len(query) > 100:
        return
    try:
        # sanitize url
        if query.endswith("/"):
            query = urljoin(query, ".")
        while "/./" in query:
            query = query.replace("/./", "/")
        # request, if this fails, it jumps to except
        req = Request(query, headers={"User-Agent": "Mozilla/5.0"})
        res = urlopen(req)
        str = res.read().decode("utf8")
        res.close()
        print("[!] Success fetching ->", query)
    except Exception as e:
        print("[!] Error fetching a submitted website (", query, ") -> ", e)
    else:
        # the website has been reached (its contents too),
        # add it to the db then
        soup = BeautifulSoup(str, 'html.parser')
        title = soup.find("title").string if soup.find(
            "title") else "No title provided"
        desc = soup.find("meta", attrs={"name": "description"})["content"] if soup.find(
            "meta", attrs={"name": "description"}) else "No description provided"
        savedb((title, query, desc))

        # now, crawl the rest of the website
        # with a limit of 40 urls (you may change this limit)
        if recrawl:
            limit = 0
            urls = []
            for tag in soup.find_all('a'):
                urls.append(tag.get('href'))
            for i in urls:
                if limit <= 40 and i != query and i:
                    if i.startswith("//"):
                        docrawl("https://" + i[2:], False)
                    elif i.startswith("https://") or i.startswith("http://"):
                        docrawl(i, False)
                    elif i.startswith('/'):
                        docrawl(urljoin(query, i), False)
                    else:
                        docrawl(urljoin(query, i), False)
                    limit += 1
