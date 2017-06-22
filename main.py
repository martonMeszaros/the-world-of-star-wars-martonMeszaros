from flask import Flask, render_template

import users
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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('error/405.html'), 405


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error/500.html', error=error), 500


if __name__ == '__main__':
    app.run()
