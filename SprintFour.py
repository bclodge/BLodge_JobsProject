import sqlite3
import plotly.express as px
import pandas as PD
from geopy import Nominatim
import SprintTwo_JobsDatabase
from geopy.extra.rate_limiter import RateLimiter
import time


geo_locator = Nominatim(user_agent='GoogleMaps')

conn, cursor = SprintTwo_JobsDatabase.open_db("job_database.sqlite")

cursor.execute(''' CREATE TABLE IF NOT EXISTS job_locations(lat REAL, long REAL);''')

cursor.execute('''SELECT company_loc FROM jobs;   ''')

rows = cursor.fetchall()
counter = 0

for data in rows:
    location = geo_locator.geocode(data)
    time.sleep(1)
    counter = counter+1
    try:
        print(location.latitude, location.longitude)
        print(counter)

        cursor.execute(''' INSERT INTO job_locations(lat, long) VALUES (?,?)''',
                       (location.latitude, location.longitude))
    except AttributeError:
        cursor.execute(''' INSERT INTO job_locations( lat, long) VALUES (?,?)''', (0.0, 0.0))





print(counter)

# target_data = SprintOne.get_jobs()
#
# framed_data = PD.DataFrame(target_data, columns=["id", "title", "type", "company", "location", "latitude", "longitude"])
#
# PD.set_option('display.max_columns', None)
#
# geocode = RateLimiter(geo_locator.geocode, min_delay_seconds=1)
#
# # framed_data["address"] = framed_data["location"].apply(geocode)
#
# fig = px.scatter_mapbox(framed_data, lat="latitude", lon="longitude", hover_name="id",
#                         hover_data=["title", "type", "company"],
#                         color_discrete_sequence=["fuchsia"], zoom=3, height=300)
# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# fig.show()
