# 7old
# search engine
#    main flask

from flask import Flask, render_template, request
from algorithm import searchdb
from crawl import docrawl

app = Flask(__name__, template_folder="templates")
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    query = request.args.get("q")
    page = request.args.get("p")
    if query is None or not query.strip():
        return render_template("index.html")
    else:
        if page is None:
            page = 1
        else:
            try:
                page = int(page)
            except:
                page = 1
        list = searchdb(query)
        start = 0 if page == 1 else 10 * (page - 1)
        results = list[start: start+10]
        pgnum = int(len(list)/10)+1
        return render_template("query.html", q=query, results=results, pgnum=pgnum, resnum=len(list))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/new")
def new():
    query = request.args.get("q")
    if query is None or not query.strip():
        return render_template("new.html")
    else:
        if len(query) <= 100:
            docrawl(query)
            return "Your URL has been submitted, it should be available for everyone!"
        else:
            return "That URL is over 100 characters long!"
