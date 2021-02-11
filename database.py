import json
import psycopg2
import logger

credentials = json.load(open("secrets.json"))["database"]

# logger.log('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(**credentials)


def get_cursor():
    return conn.cursor()


def commit():
    return conn.commit()


def create_role_table():

    curr = get_cursor()

    curr.execute(
        """
        CREATE TABLE IF NOT EXISTS roles (
            id serial PRIMARY KEY,
            userid NUMERIC NOT NULL,
            roleid NUMERIC NOT NULL
        )
        """
    )

    curr.execute(
        "DELETE FROM roles"
    )

    curr.close()


def create_role_rows(pairs):
    curr = get_cursor()
    # logger.log("Adding " + str(userid) + ", " + str(roleid))
    for userid, roleid in pairs:
        curr.execute("INSERT INTO roles (userid, roleid) VALUES ({}, {})".format(userid, roleid))

    curr.close()


def get_roles(userid):
    # logger.log("Getting roles for " + str(userid))
    curr = get_cursor()

    curr.execute("SELECT roleid FROM roles WHERE userid={}".format(userid))

    temp = curr.fetchall()
    curr.close()
    return temp


def remove_role_row(pairs):
    curr = get_cursor()
    # logger.log("Deleting " + str(userid) + ", " + str(roleid))
    for userid, roleid in pairs:
        curr.execute("DELETE FROM roles WHERE userid={} AND roleid={}".format(userid, roleid))

    curr.close()

