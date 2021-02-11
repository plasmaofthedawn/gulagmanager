import json
import psycopg2
import MySQLdb

details = json.load(open("secrets.json"))["database"]


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
        # logger.log('Connecting to the PostgreSQL database...')
        self.conn = MySQLdb.connect(host=credentials["host"], user=credentials["user"], passwd=credentials["password"],
                                    db=credentials["database"])

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
                userid VARCHAR(10) NOT NULL,
                roleid VARCHAR(10) NOT NULL
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


database = MySQL(details)
