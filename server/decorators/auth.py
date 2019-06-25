import os
from functools import wraps
from flask import request, Response


def check_auth(username, password):
    expected_username = os.environ.get("DISTILLERY_USERNAME", "joram")
    expected_password = os.environ.get("DISTILLERY_PASSWORD", "password")
    return username == expected_username and password == expected_password


def authenticate():
    """Sends a 401 response that enables basic auth"""
    msg = 'Could not verify your access level for that URL.\nYou have to login with proper credentials'
    return Response(msg, 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated
