import plotly.express as px
import pandas as PD
import SprintTwo_JobsDatabase

conn, cursor = SprintTwo_JobsDatabase.open_db("job_database.sqlite")


query = PD.read_sql_query('''SELECT * FROM jobs''', conn)

dataframe_from_table = PD.DataFrame(query, columns=["job_id", "job_type", "job_url", "created_at",
                                                    "company_posted", "job_loc", "job_title",
                                                    "Latitude", "Longitude"])


PD.set_option('display.max_columns', None)

print(dataframe_from_table)

fig = px.scatter_mapbox(dataframe_from_table, lat="Latitude", lon="Longitude", hover_name="job_id",
                        hover_data=["job_title", "job_type", "company_posted", "created_at"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()
