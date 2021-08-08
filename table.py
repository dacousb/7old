# 7old
# search engine
#  db generator

import sys
import sqlite3 as sl


def savedb(sitedata):
    con = sl.connect("results.db")
    cur = con.cursor()
    sql = "INSERT OR REPLACE INTO RESULT (title, url, desc) values(?, ?, ?)"
    try:
        cur.executemany(sql, [sitedata])
    except Exception as e:
        print("[!] Error updating database ->", e)

    con.commit()
    con.close()


def loaddb():
    # -db argument creates a new blank database
    con = sl.connect("results.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE RESULT (
            title TEXT,
            url TEXT UNIQUE,
            desc TEXT
        );
    """)
    sql = "INSERT INTO RESULT (title, url, desc) values(?, ?, ?)"
    data = [
        ("Wikipedia", "https://www.wikipedia.org",
         "Wikipedia is a free online encyclopedia, created and edited by volunteers around the world and hosted by the Wikimedia Foundation.")
    ]
    cur.executemany(sql, data)

    rows = cur.execute("SELECT * FROM RESULT")
    for row in rows:
        print(row)

    con.commit()
    con.close()


if len(sys.argv) == 2:
    if sys.argv[1] == "-db":
        if input("This can break your current results.db database! Continue? (y/N) ").lower() == "y":
            loaddb()
        else:
            print("No changes were made")
    else:
        print(" * Table module loaded, are you running this yourself? Create a blank database with -db")
else:
    print("Create a blank database with -db")
