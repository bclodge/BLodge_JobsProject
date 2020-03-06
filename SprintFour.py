import sqlite3
import plotly.express as px
import pandas as PD
from geopy import Nominatim
import SprintTwo_JobsDatabase
from geopy.extra.rate_limiter import RateLimiter
import time

import SprintOne

#SprintOne.main()


conn, cursor = SprintTwo_JobsDatabase.open_db("job_database.sqlite")


query = PD.read_sql_query('''SELECT * FROM jobs''', conn)

dataframe_from_table = PD.DataFrame(query, columns=["Job_ID", "Job_Type", "Job_Url", "Created_at",
                                                    "Company_posted", "Job_Location", "Job_Title",
                                                    "Latitude", "Longitude"])


PD.set_option('display.max_columns', None)

print(dataframe_from_table)

fig = px.scatter_mapbox(dataframe_from_table, lat="Latitude", lon="Longitude", hover_name="Job_ID",
                        hover_data=["Job_Title", "Job_Type", "Company_posted", "Created_at"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()
