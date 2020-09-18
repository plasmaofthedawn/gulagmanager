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


def create_role_table(curr):
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


def create_role_row(curr, userid, roleid):
    # logger.log("Adding " + str(userid) + ", " + str(roleid))
    curr.execute("INSERT INTO roles (userid, roleid) VALUES ({}, {})".format(userid, roleid))


def get_roles(curr, userid):
    # logger.log("Getting roles for " + str(userid))
    curr.execute("SELECT roleid FROM roles WHERE userid={}".format(userid))
    return curr.fetchall()


def remove_role_row(curr, userid, roleid):
    # logger.log("Deleting " + str(userid) + ", " + str(roleid))
    curr.execute("DELETE FROM roles WHERE userid={} AND roleid={}".format(userid, roleid))
