from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


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
