import sqlite3

conn = sqlite3.connect('earthquakes.db')
curr = conn.cursor()

def delete_all_earthquakes():
    curr.execute("DELETE FROM earthquakes")
    curr.execute("DELETE FROM daily_earthquakes")
    conn.commit()

def init_db():
    curr.execute('''
        CREATE TABLE IF NOT EXISTS earthquakes (
            id TEXT PRIMARY KEY,
            mag REAL,
            mag_bucket TEXT,
            place TEXT,
            longitude REAL,
            latitude REAL,
            depth REAL,
            date TEXT,
            time INTEGER,
            updated INTEGER,
            tz TEXT,
            url TEXT,
            status TEXT
        )
    ''')

    curr.execute('''
        CREATE TABLE IF NOT EXISTS daily_earthquakes (
            date TEXT PRIMARY KEY,
            mag_bucket TEXT,
            num_earthquakes INTEGER
        )
    ''')

    conn.commit()

def updated_earthquakes(earthquakes):
    updated_earthquakes = []
    for earthquake in earthquakes:
        res = curr.execute("SELECT updated FROM earthquakes WHERE id = ?", (earthquake['id'],))
        existing = res.fetchall()
        if not existing:
            continue
        if earthquake['updated'] != existing[0][0]:
            updated_earthquakes.append(earthquake)
    return updated_earthquakes

def new_earthquakes(earthquakes):
    new_earthquakes = []
    for earthquake in earthquakes:
        res = curr.execute("SELECT id FROM earthquakes WHERE id = ?", (earthquake['id'],))
        existing = res.fetchall()
        if not existing:
            new_earthquakes.append(earthquake)
    return new_earthquakes

def insert_earthquakes(earthquakes):
    curr.executemany('''
        INSERT INTO earthquakes (id, mag, mag_bucket, place, longitude, latitude, depth, date, time, updated, tz, url, status) VALUES (:id, :mag, :mag_bucket, :place, :longitude, :latitude, :depth, :date, :time, :updated, :tz, :url, :status)
    ''', earthquakes)
    conn.commit()

def insert_daily_earthquakes(daily_earthquakes):
    curr.executemany('''
        INSERT OR REPLACE INTO daily_earthquakes (date, mag_bucket, num_earthquakes) VALUES (:date, :mag_bucket, :num_earthquakes)
    ''', daily_earthquakes)
    conn.commit()