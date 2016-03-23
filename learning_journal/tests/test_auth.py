from passlib.hash import sha256_crypt
import os


def test_no_access_to_view(app):
    response = app.get('/entries/1/edit', status=403)
    assert response.status_code == 403


def test_password_exists(auth_env):
    assert os.environ.get('AUTH_PASSWORD', None) is not None


def test_user_exists(auth_env):
    assert os.environ.get('AUTH_USERNAME', None) is not None


def test_stored_encrypt(auth_env):
    assert os.environ.get('AUTH_PASSWORD', None) != 'secret'


def test_verify_password_success(auth_env):
    encrypted = sha256_crypt.encrypt("secret")
    password = 'secret'
    assert sha256_crypt.verify(password, encrypted)


def test_get_login(app):
    response = app.get('/login')
    assert response.status_code == 200


def test_edit_permission(authenticated_app, new_entry):
    new_entry_id = new_entry.id
    response = authenticated_app.get('/entries/{}/edit'.format(new_entry_id))
    assert response.status_code == 200


def test_login_redirects(app, auth_env):
    data = {'username': 'admin', 'password': 'secret'}
    response = app.post('/login', data)
    headers = response.headers
    domain = "http://localhost"
    actual_path = headers.get('Location', '')[len(domain):]
    assert actual_path == '/'


def test_post_success_authtkt(app, auth_env):
    data = {'username': 'admin', 'password': 'secret'}
    response = app.post('/login', data)
    headers = response.headers
    cookies_set = headers.getall('Set-Cookie')
    assert cookies_set
    for cookie in cookies_set:
        if cookie.startswith('auth_tkt'):
            break
    else:
        assert False
