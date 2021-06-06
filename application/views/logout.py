from flask import redirect
from flask_login import login_required, logout_user

from application import app, login_manager


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')
