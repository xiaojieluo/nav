# from nav import app
import nav
from nav.model import User
import pytest
import functools


@pytest.fixture(scope='module')
def data(request):
    data = {'username': 'test', 'password': 'test'}
    def clean(data = data):
        user = User.find(username = data.get('username'))
        if user:
            user.delete()
    request.addfinalizer(clean)
    return data

@pytest.fixture(scope='module')
def app(request):
    app = nav.app.test_client()
    return app

def test_user_register(app, data):
    register = functools.partial(app.post, '/register', follow_redirects=True)
    rv = register(data = data)
    assert 'successful' in str(rv.data)
    rv = register(data = data)
    assert 'failed' in str(rv.data)

def test_user_login(app, data):
    login = functools.partial(app.post, '/login', follow_redirects=True)
    rv = login(data = data)
    assert 'welcome' in str(rv.data)
    rv = login(data = {'username':'xxxxxxx'})
    assert 'failed' in str(rv.data)

def test_user_logout(app, data):
    logout = functools.partial(app.get, '/logout', follow_redirects=True)
    rv = logout(data = data)
    assert 'successful' in str(rv.data)
