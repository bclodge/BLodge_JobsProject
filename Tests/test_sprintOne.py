import SprintOne
import SprintTwo_JobsDatabase
import sqlite3


"""def test_get_jobs():
    SprintOne.main()


def test_job_name():
    SprintOne.check_jobs()

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


test_table_exists()
test_data_in_db()
