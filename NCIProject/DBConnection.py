import psycopg2


class DBConnection:
    @staticmethod
    def connect_dbs():
        try:
            conn = psycopg2.connect(database="ev_ireland", user="nciadmin@nciproject", password="Nciproject01?",
                                    host="nciproject.postgres.database.azure.com", port="5432")
            print("Connected to Database")
            return conn
        except:
            print("Failed to connect to DB")
            raise ConnectionError

