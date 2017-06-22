import hashlib
from random import choice
from string import ascii_letters, digits

from flask import redirect, render_template, request, session

from db_connection import connect_to_db
SALT_CHARS = ascii_letters + digits


def hash_password(password, salt):
    hasher = hashlib.sha1()
    hasher.update(bytes(password + salt, 'utf-8'))
    return hasher.hexdigest()


@connect_to_db
def check_existing_usernames(username):
    return ("SELECT id FROM users WHERE username = %s;", [username])


def username_already_exists(username):
    if len(check_existing_usernames(username)) > 0:
        return True
    return False


@connect_to_db
def new_user(user_data):
    return (
        '''
        INSERT INTO users 
            (username, password, salt) 
        VALUES (%(username)s, %(password)s, %(salt)s);
        ''',
        user_data
    )


@connect_to_db
def user_in_database_query(username):
    return (
        '''
        SELECT id 
        FROM users 
        WHERE username = %s;
        ''',
        [username]
    )


def user_in_database(username):
    if len(user_in_database_query(username)) > 0:
        return True
    return False


@connect_to_db
def get_user_salt_query(username):
    return (
        '''
        SELECT salt 
        FROM users 
        WHERE username = %s;
        ''',
        [username]
    )


def get_user_salt(username):
    return get_user_salt_query(username)[0][0]


@connect_to_db
def correct_credentials_query(user_data):
    return (
        '''
        SELECT id 
        FROM users 
        WHERE username = %(username)s AND password = %(password)s;
        ''',
        user_data
    )


def correct_credentials(user_data):
    if len(correct_credentials_query(user_data)) > 0:
        return True
    return False


def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_data = {
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }
        if not (
                user_data['username'] is None and
                user_data['password'] is None
        ):
            if user_in_database(user_data['username']):
                user_data['salt'] = get_user_salt(user_data['username'])
                user_data['password'] = hash_password(user_data['password'], user_data['salt'])
                if correct_credentials(user_data):
                    if session.get('user'):
                        session.pop('user', None)
                    session['user'] = user_data['username']
                    return redirect('/')
                else:   # Incorrect credentials
                    pass
            else:   # User doesn't exist
                pass
        else:   # Missing input
            pass
        return render_template('login.html')


def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        user_data = {
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }
        password_check = request.form.get('password-check')
        if not (
                user_data['username'] is None or
                user_data['password'] is None or
                password_check is None
        ):
            if not username_already_exists(user_data['username']):
                if user_data['password'] == password_check:
                    del password_check
                    user_data['salt'] = ''.join([choice(SALT_CHARS) for _ in range(8)])
                    user_data['password'] = hash_password(
                        user_data['password'], user_data['salt']
                    )
                    new_user(user_data)
                    session['user'] = user_data['username']
                    return redirect('/')
                else:   # Two passwords didn't match
                    pass
            else:   # Username already exists
                pass
        else:   # Missing input
            pass
        return render_template('register.html')


def logout():
    if session.get('user'):
        session.pop('user', None)
    return redirect('/')
