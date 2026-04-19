import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect('earthquakes.db')
    curr = conn.cursor()

    res = curr.execute("SELECT * FROM earthquakes")
    print(len(res.fetchall()))

    res = curr.execute("SELECT * FROM daily_earthquakes")
    print(len(res.fetchall()))