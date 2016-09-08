from flask import render_template, app
from datetime import datetime


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', current_time=datetime.utcnow()), 404


@app.errorhandler(500)
def internal_server_error(e):
    return (render_template('500.html', current_time=datetime.utcnow()), 500)
