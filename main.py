from flask import Flask, redirect, render_template, request, session
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        pass


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username', None)
    return redirect('/')


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
