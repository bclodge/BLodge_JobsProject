import SprintTwo_JobsDatabase
import sqlite3
# import SprintOne


"""def test_get_jobs():
    SprintOne.main()


def test_job_name():
    SprintOne.check_jobs()

these are the tests from sprint one, can be used by importing the SprintOne.py file
"""


def test_table_exists():
    conn = sqlite3.connect('Job_database.sqlite')
    cursor = conn.cursor()

    SprintTwo_JobsDatabase.setup_db(cursor)

    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='jobs' ''')

    assert (cursor.fetchone()[0] == 1)


def test_data_in_db():
    conn = sqlite3.connect('Job_database.sqlite')
    cursor = conn.cursor()

    SprintTwo_JobsDatabase.setup_db(cursor)

    cursor.execute('''SELECT * FROM jobs WHERE job_id='39231b99-2aa9-4652-b6ec-2254db9f781b';   ''')

    rows = cursor.fetchall()
    for data in rows:
        assert data == "39231b99-2aa9-4652-b6ec-2254db9f781b"


def test_SprintThree_db_exsists():
    conn = sqlite3.connect('RSS_feed_SprintThree.sqlite')
    cursor = conn.cursor()

    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='RSS_pull' ''')

    assert (cursor.fetchone()[0] == 1)


test_table_exists()
test_data_in_db()
test_SprintThree_db_exsists()
