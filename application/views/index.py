from flask import redirect

from application import app


@app.route('/')
def open_application():
    return redirect('/workshops')
