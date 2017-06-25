from flask import Flask, render_template, session

import users
import vote
app = Flask(__name__)
app.secret_key = ':3{ET|:Ha7:_@~Rma7lPxz$lg-J|V,'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return users.login()


@app.route('/register', methods=['GET', 'POST'])
def register():
    return users.register()


@app.route('/logout')
def logout():
    return users.logout()


@app.route('/vote/<int:planet_id>', methods=['POST'])
def vote_for_planet(planet_id):
    if session.get('user'):
        return vote.new_vote(planet_id)
    else:
        pass


@app.route('/votes')
def get_votes():
    return vote.get_votes()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('error/405.html'), 405


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error/500.html', error=error), 500
