import feedparser
import sqlite3
from geopy import Nominatim
import time


geo_locator = Nominatim(user_agent='GoogleMaps')

parsed_feed = feedparser.parse("https://stackoverflow.com/jobs/feed")
connection = sqlite3.connect('job_database.sqlite')
cursor = connection.cursor()


def makeRSSTable():
    cursor.execute(''' CREATE TABLE IF NOT EXISTS RSS_pull(\
       job_id TEXT PRIMARY KEY, job_type TEXT, job_url TEXT, created_at TEXT, 
            company_posted TEXT,  location TEXT, job_title TEXT, latitude REAL, longitude REAL);''')

    cursor.execute('DELETE FROM RSS_pull;')  # clears the table before running, error arose on unique id of job links on
    # rerun

    for entries in parsed_feed['items']:
        print(entries)
        id = entries.id
        title = entries.title
        link = entries.link
        created_at = entries.published
        company_posted = entries.author
        description = entries.description

        # print(id)
        # print(created_at)
        # print(company_posted)
        # print(type(company_posted))
        string = title

        first_pos = string.rfind("(")
        # position of closing square bracket
        last_pos = string.rfind(")")
        # printing the text between two square brackets

        temp_location_holder = geo_locator.geocode(string[first_pos + 1: last_pos])

        time.sleep(2.75)

        with connection:
            try:
                cursor.execute('''INSERT INTO RSS_pull (job_id, job_type, job_url, created_at, company_posted, location,\
                 job_title, latitude, longitude)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                               (id, "Full Time", link, created_at, company_posted, string[first_pos + 1: last_pos],
                                title,
                                temp_location_holder.latitude,
                                temp_location_holder.longitude))

            except AttributeError:
                cursor.execute('''INSERT INTO RSS_pull (job_id, job_type, job_url, created_at,
            company_posted,  location, job_title, latitude, longitude) ''' 'VALUES (?, '
                               '?, ?, ?, ?, ?, ?, ?, ?);''',
                               (id, "Remote", link, created_at, company_posted, string[first_pos + 1: last_pos],
                                title,
                                0.0, 0.0))


def CopyTables():

    cursor.execute(''' CREATE TABLE IF NOT EXISTS DualTable(\
            job_id TEXT PRIMARY KEY,\
            job_type TEXT NOT NULL,\
            job_url TEXT NOT NULL,\
            created_at TEXT NOT NULL, company_posted TEXT NOT NULL, company_loc TEXT NOT NULL, job_title TEXT NOT NULL,
             Latitude REAL, Longitude REAL);''')
    cursor.execute('''DELETE FROM DualTable''')
    cursor.execute('''INSERT INTO DualTable SELECT * FROM jobs''')


def UnionTable():
    cursor.execute(''' SELECT DualTable.job_id, DualTable.job_type, DualTable.job_url, DualTable.created_at,
        DualTable.company_posted,  DualTable.company_loc, DualTable.job_title, DualTable.latitude, DualTable.longitude
         FROM DualTable UNION SELECT RSS_pull.job_id, RSS_pull.job_type, RSS_pull.job_url, RSS_pull.created_at,
            RSS_pull.company_posted,  RSS_pull.location, RSS_pull.job_title, RSS_pull.latitude, RSS_pull.longitude
             FROM RSS_pull;''')
    connection.commit()


CopyTables()
UnionTable()
# Commit your changes to the program
connection.commit()
# Close the cursor_object
connection.close()
