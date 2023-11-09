from functools import wraps

import requests

from users_service.models import User
from flask import session, flash, redirect, url_for


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'logged_in' not in session:
                flash('Unauthorized, Please login', 'danger')
                return redirect(url_for('login'))
            user = User.query.filter_by(username=session['username']).first()
            if user.role not in roles:
                flash('Unauthorized, insufficient role', 'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper
