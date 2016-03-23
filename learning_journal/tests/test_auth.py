import pytest
import webtest
import os
from passlib.apps import custom_app_context as pwd_context

from learning_journal import main


@pytest.fixture()
def app():
    settings = {}
    app = main({}, **settings)
    return webtest.TestApp(app)


@pytest.fixture()
def auth_env():
    os.environ['AUTH_PASSWORD'] = pwd_context.encrypt('secret')
    os.environ['AUTH_USERNAME'] = 'admin'


@pytest.fixture()
def authenticated_app(app, auth_env):
    data = {'username': 'admin', 'password': 'secret'}
    app.post('/login', data)
    return app


def test_no_access_to_view(app):
    response = app.get('/entries/1/edit', status=403)
    assert response.status_code == 403


def test_access_to_view(app):
    response = app.get('/entries/1/edit')
    assert response.status_code == 200


def test_password_exists(auth_env):
    assert os.environ.get('AUTH_PASSWORD', None) is not None


def test_user_exists(auth_env):
    assert os.environ.get('AUTH_USERNAME', None) is not None


def test_stored_encrypt(auth_env):
    assert os.environ.get('AUTH_PASSWORD', None) != 'secret'


# def test_check_pw_success(auth_env):
#     from foobar.security import check_pw
#     password = 'secret'
#     assert check_pw(password)


# def test_check_pw_fails(auth_env):
#     from foobar.security import check_pw
#     password = 'faaaaailure'
#     assert not check_pw(password)


def test_get_login(app):
    response = app.get('/login')
    assert response.status_code == 200


def test_post_login(app, auth_env):
    data = {'username': 'admin', 'password': 'secret'}  # form fields
    response = app.post('/login', data)
    assert response.status_code == 302


def test_login_redirects(app, auth_env):
    data = {'username': 'admin', 'password': 'secret'}  # form fields
    response = app.post('/login', data)
    headers = response.headers
    domain = "http://localhost"
    actual_path = headers.get('Location', '')[len(domain):]
    assert actual_path == '/'


def test_post_success_authtkt(app, auth_env):
    data = {'username': 'admin', 'password': 'secret'}  # form fields
    response = app.post('/login', data)
    headers = response.headers
    cookies_set = headers.getall('Set-Cookie')
    assert cookies_set
    for cookie in cookies_set:
        if cookie.startswith('auth_tkt'):
            break
    else:
        assert False


def test_post_login_fail(app, auth_env):
    data = {'username': 'admin', 'password': ':('}  # form fields
    response = app.post('/login', data)
    assert response.status_code == 200
