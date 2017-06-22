from os import environ

from flask import abort
import psycopg2


def connect_to_db(wrapped_function):
    def establish_db_connection(*args, **kwargs):
        _db_connection = None
        _cursor = None
        connection_data = {
            'dbname': environ.get('MY_PSQL_DBNAME'),
            'user': environ.get('MY_PSQL_USERNAME'),
            'host': environ.get('MY_PSQL_HOST'),
            'password': environ.get('MY_PSQL_PASSWORD')
        }
        for key, value in connection_data.items():
            if value is None:
                abort(500, 'No database configuration found!')
                break
        connection_string = "dbname='{dbname}' user='{user}' host='{host}' password='{password}'"
        connection_string = connection_string.format(**connection_data)
        try:
            _db_connection = psycopg2.connect(connection_string)
            _db_connection.autocommit = True
            _cursor = _db_connection.cursor()
            _cursor.execute(
                wrapped_function(*args, **kwargs)[0],   # query or command
                wrapped_function(*args, **kwargs)[1]    # parameters
            )
            if 'SELECT' in wrapped_function(*args, **kwargs)[0]:
                result = _cursor.fetchall()
            _cursor.close()
            _db_connection.close()
            if 'SELECT' in wrapped_function(*args, **kwargs)[0]:
                return result
        except psycopg2.DatabaseError:
            abort(500, 'Couldn\'t connect to database')
    return establish_db_connection
