from db_connection import connect_to_db


@connect_to_db
def get_user_by_id(id):
    return (
        '''
        SELECT id, username, password, salt
        FROM users
        WHERE id = %s;
        ''',
        [id]
    )


@connect_to_db
def get_user_by_username(username):
    return (
        '''
        SELECT id, username, password, salt
        FROM users
        WHERE username = %s;
        ''',
        [username]
    )


@connect_to_db
def new_user(user_data):
    return (
        '''
        INSERT INTO users
            (username, password, salt)
        VALUES (
            %(username)s, %(password)s, %(salt)s
        );
        ''',
        user_data
    )


@connect_to_db
def check_credentials(user_data):
    return (
        '''
        SELECT id
        FROM users
        WHERE username = %(username)s AND password = %(password)s;
        ''',
        user_data
    )
