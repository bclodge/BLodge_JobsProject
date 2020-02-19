import feedparser
import sqlite3

parsed_feed = feedparser.parse("https://stackoverflow.com/jobs/feed")
connection = sqlite3.connect('RSS_feed_SprintThree.sqlite')
cursor = connection.cursor()

cursor.execute('DELETE FROM RSS_pull;')  # clears the table before running, error arose on unique id of job links on
# rerun

for entries in parsed_feed['items']:
    title = entries.title
    link = entries.link
    description = entries.description

    print(link)
    print(title)
    print(description)

    with connection:
        cursor.execute('INSERT INTO main.RSS_pull (title, link, description) '
                       'VALUES (?, ?, ?);', (entries['title'], entries['link'], entries['description']))

# Commit your changes to the program
connection.commit()
# Close the cursor_object
connection.close()
