import sqlite3
import plotly.express as px
import pandas as PD
import SprintTwo_JobsDatabase
import dash
import dash_core_components as dashCoreComp
import dash_html_components as html
import geopy.distance as geoDist
from typing import Tuple


def establishConnection() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    conn = sqlite3.connect("job_database.sqlite")  # connects to db or makes new one
    cursor = conn.cursor()
    return conn, cursor


def createDataFrame():
    conn, cursor = establishConnection()
    query = PD.read_sql_query('''SELECT * FROM DualTable''', conn)

    dataframe_from_table = PD.DataFrame(query, columns=["job_id", "job_type", "job_url", "created_at",
                                                        "company_posted", "job_loc", "job_title",
                                                        "Latitude", "Longitude"])
    return dataframe_from_table


def createMap():
    data_frame = createDataFrame()
    PD.set_option('display.max_columns', None)

    fig = px.scatter_mapbox(data_frame, lat="Latitude", lon="Longitude", hover_name="job_id",
                            hover_data=["job_title", "job_type", "company_posted", "created_at"],
                            color_discrete_sequence=["fuchsia"], title="All Jobs", zoom=3, height=600)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


# creates a new table to make plotting easier.
def makeFiftyMileRadiusTable():
    conn, cursor = establishConnection()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS FiftyMileRadius(\
        job_id TEXT PRIMARY KEY,\
        job_type TEXT NOT NULL,\
        job_url TEXT NOT NULL,\
        created_at TEXT NOT NULL, company_posted TEXT NOT NULL, company_loc TEXT NOT NULL, job_title TEXT NOT NULL,
         Latitude REAL, Longitude REAL);''')

    SprintTwo_JobsDatabase.close_db(conn)


# creates another table for pandas to read easier
def makeDistancedTable():
    conn, cursor = establishConnection()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS DistanceTable(\
        job_id TEXT PRIMARY KEY,\
        job_type TEXT NOT NULL,\
        job_url TEXT NOT NULL,\
        created_at TEXT NOT NULL, company_posted TEXT NOT NULL, company_loc TEXT NOT NULL, job_title TEXT NOT NULL,
         Latitude REAL, Longitude REAL);''')

    SprintTwo_JobsDatabase.close_db(conn)


def insertIntoFiftyMileRadiusTable():
    makeFiftyMileRadiusTable()
    conn, cursor = establishConnection()

    cursor.execute('''DELETE FROM FiftyMileRadius''')
    cursor.execute('''INSERT INTO FiftyMileRadius SELECT * FROM DualTable''')

    SprintTwo_JobsDatabase.close_db(conn)


def insertIntoDistance():
    startingCoords = (41.9667679, -70.9661533)

    insertIntoFiftyMileRadiusTable()

    conn, cursor = establishConnection()
    cursor.execute('''DELETE FROM DistanceTable''')
    cursor.execute('''SELECT company_loc, Latitude, Longitude FROM FiftyMileRadius''')

    rows = cursor.fetchall()

    for data in rows:
        comparativeCoord = (data[1], data[2])

        distance = geoDist.distance(comparativeCoord, startingCoords).miles

        if distance <= 50:
            print(data[0])
            cursor.execute(
                f'''INSERT OR IGNORE INTO  DistanceTable SELECT * FROM FiftyMileRadius where company_loc  = "{data[0]}" ''')

    SprintTwo_JobsDatabase.close_db(conn)


def plotFiftyMileRadius():
    conn, cursor = establishConnection()

    query = PD.read_sql_query('''SELECT * FROM DistanceTable''', conn)

    cursor.execute('''SELECT * FROM DistanceTable ''')

    rows = cursor.fetchall()

    for columns in rows:
        print(columns)
    print(query)

    dataframe_from_table = PD.DataFrame(query, columns=["job_id", "job_type", "job_url", "created_at",
                                                        "company_posted", "job_loc", "job_title",
                                                        "Latitude", "Longitude"])

    fig = px.scatter_mapbox(dataframe_from_table, lat="Latitude", lon="Longitude", hover_name="job_id",
                            hover_data=["job_title", "job_type", "company_posted", "created_at"],
                            color_discrete_sequence=["fuchsia"],title="50 Mile radius", zoom=3, height=600)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


def printRemoteJobs():
    conn, cursor = establishConnection()

    cursor.execute(''' SELECT * from DualTable WHERE Latitude = 0.0 AND Longitude = 0.0''')

    rows = cursor.fetchall()

    print("Printing Remote Jobs")
    print("\n")
    for data in rows:
        print(data)


def printandPlotSelectCompany():
    conn, cursor = establishConnection()

    company1 = "Picnic"
    company2 = "Microsoft"

    query = PD.read_sql_query(f'''SELECT * FROM DualTable WHERE company_posted = "{company1}" 
    OR company_posted = "{company2}" ''', conn)

    print("\n")
    print(f"These are the jobs posted for {company1} and {company2} ")

    print(query)

    dataframe_from_table = PD.DataFrame(query, columns=["job_id", "job_type", "job_url", "created_at",
                                                        "company_posted", "job_loc", "job_title",
                                                        "Latitude", "Longitude"])

    fig = px.scatter_mapbox(dataframe_from_table, lat="Latitude", lon="Longitude", hover_name="job_id",
                            hover_data=["job_title", "job_type", "company_posted", "created_at"],
                            color_discrete_sequence=["fuchsia"], title=f"{company1} and {company2} Job Locations",
                            zoom=3, height=600)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()




# createMap()
# makeDistancedTable()
# insertIntoDistance()
# makeFiftyMileRadiusTable()
# plotFiftyMileRadius()
printRemoteJobs()
printandPlotSelectCompany()
