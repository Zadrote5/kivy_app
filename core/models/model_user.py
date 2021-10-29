from core.db.db import Database


class User:
    db = Database()

    def __init__(self, pk, name, surname, born):
        self.name = name
        self.surname = surname
        self.born = born
        self.id = pk

    def __str__(self):
        return ' '.join((self.name, self.surname, self.born))

    @classmethod
    def get_all_users(cls):
        users_db = cls.db.get_all_records()
        users = []
        for user_db in users_db:
            user = cls(user_db['id'], user_db['name'], user_db['surname'], user_db['born'])
            users.append(user)
        return users

    @classmethod
    def add_user(cls, name, surname, born):
        cls.db.add_new_user(name, surname, born)

    @classmethod
    def delete_user(cls, pk):
        cls.db.delete_user(pk)

    @classmethod
    def update_user(cls, pk, name, surname, born):
        cls.db.update_user(pk, name, surname, born)





