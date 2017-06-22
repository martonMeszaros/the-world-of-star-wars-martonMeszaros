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


def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
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
                else:   # two passwords didn't match
                    pass
            else:
                pass    # username already exists
        return render_template('register.html')


def logout():
    if session.get('user'):
        session.pop('user', None)
    return redirect('/')
