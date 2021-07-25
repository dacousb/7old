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
    if query is None or not query.strip():
        return render_template("index.html")
    else:
        return render_template("query.html", q=query, results=searchdb(query))

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
            return "Your URL has been submitted, it should be available for everyone in some minutes!"
        else:
            return "That URL is over 100 characters long!"
