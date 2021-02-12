import json
import os

import psycopg2
import MySQLdb

details = json.loads(os.environ.get('SECRETS'))["database"]


class PostgreSQL:

    def __init__(self, credentials):
        # logger.log('Connecting to the PostgreSQL database...')
        self.conn = psycopg2.connect(**credentials)

    def get_cursor(self):
        return self.conn.cursor()

    def commit(self):
        return self.conn.commit()

    def create_role_table(self):

        curr = self.get_cursor()

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

    def create_role_rows(self, pairs):
        curr = self.get_cursor()
        # logger.log("Adding " + str(userid) + ", " + str(roleid))
        for userid, roleid in pairs:
            curr.execute("INSERT INTO roles (userid, roleid) VALUES ({}, {})".format(userid, roleid))

        curr.close()

    def get_roles(self, userid):
        # logger.log("Getting roles for " + str(userid))
        curr = self.get_cursor()

        curr.execute("SELECT roleid FROM roles WHERE userid={}".format(userid))

        temp = curr.fetchall()
        curr.close()
        return temp

    def remove_role_row(self, pairs):
        curr = self.get_cursor()
        # logger.log("Deleting " + str(userid) + ", " + str(roleid))
        for userid, roleid in pairs:
            curr.execute("DELETE FROM roles WHERE userid={} AND roleid={}".format(userid, roleid))

        curr.close()


class MySQL:

    def __init__(self, credentials):
        self.conn = MySQLdb.connect(host=credentials["host"], user=credentials["user"], passwd=credentials["password"],
                                    db=credentials["database"], ssl=False)

    def get_cursor(self):
        return self.conn.cursor()

    def commit(self):
        return self.conn.commit()

    def create_role_table(self):

        curr = self.get_cursor()

        curr.execute(
            """
            CREATE TABLE IF NOT EXISTS roles (
                id serial PRIMARY KEY,
                userid BIGINT NOT NULL,
                roleid BIGINT NOT NULL
            )
            """
        )

        curr.execute(
            "DELETE FROM roles"
        )

        curr.close()

    def create_role_rows(self, pairs):

        if not pairs:
            return

        curr = self.get_cursor()
        # TODO: see if this cleans up the same in postgresql.
        # i don't plan on using postgresql but it'll be neat to know for the future
        curr.execute("INSERT INTO roles (userid, roleid) VALUES " +
                     ", ".join(["({}, {})".format(userid, roleid) for userid, roleid in pairs]))
        curr.close()

    def get_roles(self, userid):
        curr = self.get_cursor()

        curr.execute("SELECT roleid FROM roles WHERE userid={}".format(userid))

        temp = curr.fetchall()
        curr.close()
        return temp

    def remove_role_row(self, pairs):
        curr = self.get_cursor()
        # logger.log("Deleting " + str(userid) + ", " + str(roleid))
        for userid, roleid in pairs:
            curr.execute("DELETE FROM roles WHERE userid={} AND roleid={}".format(userid, roleid))

        curr.close()


database = MySQL(details)
