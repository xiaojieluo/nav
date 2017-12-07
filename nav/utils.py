from functools import wraps
from flask import g, request, redirect, url_for, session, abort
from nav import app
from pprint import pprint

def authenticated(func):
    '''
    检测用户是否登陆
    1. must login
    '''
    print(func)
    @wraps(func)
    def decorated_function(*args, **kw):
        print(args)
        print(kw)
        # if g.user is None:
        if 'uid' not in session:
            return redirect(url_for('login', next = request.url))
        return func(*args, **kw)
    return decorated_function

def user_themeselves(uid):
    '''
    检测已登陆用户是否是本人
    '''
    if uid == session['uid']:
        return
    else:
        abort(403)
