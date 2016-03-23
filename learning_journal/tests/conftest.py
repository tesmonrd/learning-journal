# -*- coding: utf-8 -*-
import pytest
from sqlalchemy import create_engine
import os
from passlib.hash import sha256_crypt


from learning_journal.models import DBSession, Base, Entry


TEST_DATABASE = 'postgresql://ricktesmond:@localhost:5432/testdb'


@pytest.fixture(scope='session')
def sqlengine(request):
    engine = create_engine(TEST_DATABASE)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
def dbtransaction(request, sqlengine):
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)
    return connection


@pytest.fixture(scope='function')
def new_entry(request):
    new_entry = Entry(title='something', text='whatever')
    DBSession.add(new_entry)
    DBSession.flush()

    def teardown():
        DBSession.query(Entry).filter(Entry.id == new_entry.id).delete()
        DBSession.flush()

    request.addfinalizer(teardown)
    return new_entry


@pytest.fixture()
def app(dbtransaction):
    from webtest import TestApp
    from learning_journal import main
    fake_settings = {'sqlalchemy.url': TEST_DATABASE}
    os.environ['JOURNAL_DB'] = TEST_DATABASE
    app = main({}, **fake_settings)
    return TestApp(app)


@pytest.fixture()
def auth_env():
    os.environ['AUTH_PASSWORD'] = sha256_crypt.encrypt('secret')
    os.environ['AUTH_USERNAME'] = 'admin'


@pytest.fixture()
def authenticated_app(app, auth_env):
    data = {'username': 'admin', 'password': 'secret'}
    app.post('/login', data, status='3*')
    return app
