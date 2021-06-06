from flask import redirect, url_for

from application import app


@app.route('/')
def open_application():
    return redirect('/workshops')
