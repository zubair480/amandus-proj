import sqlite3

class EtihadDb:
    def __init__(self, database_name = "db.db"):
        self.database_name = database_name
        pass

    def create_db(self):
        con = self.create_connection()
        con.execute("DROP TABLE IF EXISTS files")
        con.execute("CREATE TABLE  files(filename VARCHAR(200), content TEXT) ")
        con.commit()

    def add_file(self, filename, content):
        con = self.create_connection()
        sql = ''' INSERT INTO files(filename, content)
                   VALUES(?,?) '''

        con.execute(sql, (filename, content))
        con.commit()


    def update(self, filename, content):
        pass

    def get_file_list(self):
        con = self.create_connection()

        cur = con.cursor()
        cur.execute("SELECT * FROM files")
        rows = cur.fetchall()
        return rows

    def get_file(self, filename):
        con = self.create_connection()

        cur = con.cursor()
        cur.execute(f"SELECT * FROM files WHERE filename = '{filename}' LIMIT 1") # TODO: SQL injection!!!
        rows = cur.fetchall()
        if len(rows) == 1:
            return rows[0][1]
        return None

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
        except BaseException as error:
            print(error)

        return conn

