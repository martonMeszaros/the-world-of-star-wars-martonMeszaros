import hashlib
from random import choice
from string import ascii_letters, digits

from flask import redirect, render_template, request, session

import users_data_manager


def hash_password(password, salt):
    hasher = hashlib.sha1()
    hasher.update(bytes(password + salt, 'utf-8'))
    return hasher.hexdigest()


def user_in_database(username):
    if len(users_data_manager.get_user_by_username(username)) > 0:
        return True
    return False


def get_user_salt(username):
    return users_data_manager.get_user_by_username(username)[0][3]


def correct_credentials(user_data):
    if len(users_data_manager.check_credentials(user_data)) > 0:
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
                user_data['username'] is None or
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
            'password': request.form.get('password'),
            'password_check': request.form.get('password-check')
        }
        if not (
                user_data['username'] is None or
                user_data['password'] is None or
                user_data['password_check'] is None
        ):
            if not user_in_database(user_data['username']):
                if user_data['password'] == user_data['password_check']:
                    del user_data['password_check']
                    salt_characters = ascii_letters + digits
                    user_data['salt'] = ''.join([choice(salt_characters) for _ in range(8)])
                    user_data['password'] = hash_password(
                        user_data['password'], user_data['salt']
                    )
                    users_data_manager.new_user(user_data)
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
