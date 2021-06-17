from flask import request, redirect

from application import app

@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect('/signin')
    return response
