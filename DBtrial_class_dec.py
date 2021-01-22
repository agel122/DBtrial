import psycopg2
from contextlib import closing
from functools import wraps


class DBfunc:
    def __init__(self, database=None):
        if not database:
            self.database = {'dbname': 'phonebook', 'user': 'katya', 'password': 'katka', 'host': 'localhost',
                              'table': 'phonenote'}
        else:
            self.database = database

    def _output(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            data = method(*args, **kwargs)
            for i in data:
                for j in i:
                    print(j, end=' ')
                print(' ')
        return wrapper

    def _dbcommit(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            self = args[0]
            with closing(psycopg2.connect(dbname=self.database['dbname'], user=self.database['user'],
                                      password=self.database['password'], host=self.database['host'])) as conn:
                with conn.cursor() as cursor:
                    try:
                        cursor.execute(method(*args, **kwargs))
                        records = cursor.fetchall()
                    except psycopg2.ProgrammingError:
                        records = None
                    finally:
                        conn.commit()
            return records
        return wrapper

    @_dbcommit
    def add_data(self, *args):
        query = f"INSERT INTO {self.database['table']} VALUES {args}"
        return query

    @_output
    @_dbcommit
    def show_all(self):
        query = f"SELECT * FROM {self.database['table']}"
        return query

    @_output
    @_dbcommit
    def show_data(self, item, value):
        query = f"SELECT * FROM {self.database['table']} WHERE {item} = '{value}'"
        return query

    @_dbcommit
    def del_data(self, item, value):
        query = f"DELETE FROM {self.database['table']} WHERE {item} = '{value}'"
        return query

    @_dbcommit
    def upd_data(self, item, value, item_to_update, new_value_item_to_update):
        query = f"UPDATE {self.database['table']} SET {item_to_update} = '{new_value_item_to_update}'" \
                f"WHERE {item} = '{value}'"
        return query


if __name__ == '__main__':
    result = DBfunc()
    # result.show_all()
    # result.del_data('name', 'Дураков Василь Василич')
    result.show_data('name', 'Пидорков Василь Василич')
    # result.upd_data('name', 'Сидоров Петр Петрович', 'phone', '1111111')
    # result.add_data('Гнездюков Василь Василич', '89293334455', 'тестовый номер 6')
    # result.show_all()
