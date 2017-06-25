from os
import urllib

from flask import abort
import psycopg2


def connect_to_db(wrapped_function):
    def establish_db_connection(*args, **kwargs):
        try:
            urllib.parse.uses_netloc.append('postgres')
            url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
            _db_connection = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
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
