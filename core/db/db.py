import pymysql
from pymysql.cursors import DictCursor


class Database:

    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='zadrote5',
            db='mvc',
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        self.cur = self.connection.cursor()

    def get_all_records(self):
        self.cur.execute("SELECT * FROM users")
        records = self.cur.fetchall()
        return records

    def add_new_user(self, name, surname, born):
        query = "INSERT INTO users (name, surname, born) VALUES ('%s', '%s', '%s')"
        query = (query % (name, surname, born))
        self.cur.execute(query)
        self.connection.commit()
        return self.cur.lastrowid

    def set_id(self):
        pk = self.cur.lastrowid
        print(pk)
        return pk

    def delete_user(self, pk):
        query = "DELETE FROM users WHERE id = {id};".format(id=pk)
        self.cur.execute(query)
        self.connection.commit()

    def update_user(self, pk, name, surname, born):
        query = "UPDATE users SET name = '{name}', surname = '{surname}', born = '{born}' WHERE id = {pk};".format(name=name,
                                                                                                             surname=surname,
                                                                                                             born=born,
                                                                                                             pk=pk)
        self.cur.execute(query)
        self.connection.commit()
