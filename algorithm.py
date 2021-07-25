# 7old
# search engine algorithm
#  that gets data from DB

import sqlite3 as sl


def searchdb(q):
    con = sl.connect("results.db")
    with con:
        rows = con.execute("SELECT * FROM RESULT ORDER BY title")
        result = []
        for row in rows:
            if any(q in s for s in row):
                result.append(row)
        return result
