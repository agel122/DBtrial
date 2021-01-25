import psycopg2
from contextlib import closing
from functools import wraps
from psycopg2 import sql


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
        query = sql.SQL("INSERT INTO {table} VALUES {args}")\
            .format(table=sql.Identifier(self.database['table']), args=sql.Literal(args))
        return query

    @_output
    @_dbcommit
    def show_all(self):
        query = sql.SQL("SELECT * FROM {table}")\
            .format(table=sql.Identifier(self.database['table']))
        return query

    @_output
    @_dbcommit
    def show_data(self, item, value):
        query = sql.SQL("SELECT * FROM {table} WHERE {name} = {data}") \
            .format(table=sql.Identifier(self.database['table']),
                    name=sql.Identifier(item),
                    data=sql.Literal(value))
        return query

    @_dbcommit
    def del_data(self, item, value):
        query = sql.SQL("DELETE FROM {table} WHERE {name} = {data}")\
            .format(table=sql.Identifier(self.database['table']), name=sql.Identifier(item), data=sql.Literal(value))
        return query

    @_dbcommit
    def upd_data(self, item, value, item_to_update, new_value_item_to_update):
        query = sql.SQL("UPDATE {table} SET {name1} = {data1} WHERE {name2} = {data2}")\
            .format(table=sql.Identifier(self.database['table']),
                   name1=sql.Identifier(item_to_update), data1=sql.Literal(new_value_item_to_update),
                   name2 = sql.Identifier(item),
                   data2 = sql.Literal(value))
        return query


if __name__ == '__main__':
    result = DBfunc()
    # result.show_all()
    # result.del_data('name', 'Гнездюков Василь Василич')
    # result.show_data('name', 'Васильков Василь Василич')
    # result.upd_data('name', 'Сидоров Петр Петрович', 'phone', '99999')
    # result.add_data('Звездюков Петр Василич', '1111', 'тестовый номер 7')
    result.show_all()
