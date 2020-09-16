import json
import psycopg2

def connect():
    credentials = json.load(open("secrets.json"))["database"]

    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**credentials)

    # create a cursor
    cur = conn.cursor()

    # execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)

    return conn
