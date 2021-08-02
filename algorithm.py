# 7old
# search engine algorithm
#  that gets data from DB

import sqlite3 as sl


def searchdb(q):
    con = sl.connect("results.db")
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM RESULT ORDER BY title")
    result = []
    for row in rows:
        if (q in row[1] # URL
            and row[1].count('/') <= 3
            and (row[1].count('.') == 1
            or (row[1].startswith('https://www.')
                and row[1].count('.') == 2))
                and '?' not in row[1]):
            result.insert(0, row)
        elif any(q in s for s in row):
            result.append(row)
    con.close()
    return result
