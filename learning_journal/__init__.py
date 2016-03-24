from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
import os

from .models import (
    DBSession,
    Base,
    BaseFactory,
)


def make_session(settings):
    from sqlalchemy.orm import sessionmaker
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session = sessionmaker(bind=engine)
    return Session()


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    if 'DATABASE_URL' in os.environ:
        settings['sqlalchemy.url'] = os.environ.get('DATABASE_URL')
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    secret = os.environ.get('dsfkljfvjkvnadssvjkbavhfdlbvhfdlv', 'vndjkvbndlv')
    authentication_policy = AuthTktAuthenticationPolicy(secret)
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(
        settings=settings,
        authentication_policy=authentication_policy,
        authorization_policy=authorization_policy,
        root_factory=BaseFactory
    )
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index_route', '/')
    config.add_route('new_route', '/add')
    config.add_route('entry_route', '/entries/{id:\d+}')
    config.add_route('edit_route', '/entries/{id:\d+}/edit')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
