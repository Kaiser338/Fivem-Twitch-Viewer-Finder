import mysql.connector
import config

class Database:
    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host=config.DATABASE_CONFIG['HOST'],
                user=config.DATABASE_CONFIG['USER'],
                passwd=config.DATABASE_CONFIG['PASSWORD'],
                database=config.DATABASE_CONFIG['DATABASE'],
                port=config.DATABASE_CONFIG['PORT']
            )
            self.cursor = self.db.cursor()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db = None

    def get_whitelist(self):
        whitelist = []
        if self.db:
            try:
                sql_formula = "SELECT twitch_name FROM suspects"
                self.cursor.execute(sql_formula)
                my_result = self.cursor.fetchall()
                for row in my_result:
                    whitelist.append(row[0])
            except mysql.connector.Error as err:
                print(f"Error fetching whitelist: {err}")
        return whitelist

    def get_streamers(self):
        streamers = []
        if self.db:
            try:
                sql_formula = "SELECT name FROM streamers"
                self.cursor.execute(sql_formula)
                my_result = self.cursor.fetchall()
                for row in my_result:
                    streamers.append(bytearray.decode(row[0]))
            except mysql.connector.Error as err:
                print(f"Error fetching streamers: {err}")
        return streamers
