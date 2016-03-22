# -*- coding: utf-8 -*-
from pyramid.view import view_config
from .models import Entry, DBSession
from wtforms import Form, StringField, TextAreaField, validators
from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    authenticated_userid,
    remember,
    forget,
)


@view_config(route_name='index_route', renderer='../rick-mockups/list.jinja2')
def post_index(request):
    entries = DBSession.query(Entry).all()
    form = None
    if not authenticated_userid(request):
        form = LoginForm()
    return {'entries': entries, 'login_form': form}


@view_config(route_name='entry_route', renderer='../rick-mockups/entry.jinja2')
def view_post(request):
    entry_id = '{id}'.format(**request.matchdict)
    entry = DBSession.query(Entry).get(entry_id)
    return {'entry': entry}


@view_config(route_name='new_route', renderer='../rick-mockups/add.jinja2',
             permission='add')
def add_post(request):
    form = EntryForm(request.POST)
    if request.method == 'POST' and form.validate():
        entry = Entry()
        entry.title = form.title.data
        entry.text = form.text.data
        DBSession.add(entry)
        DBSession.flush()
        entry_id = entry.id
        url = request.route_url('entry_route', id=entry_id)
        return HTTPFound(url)
    return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='edit_route', renderer='../rick-mockups/add.jinja2',
             permission='edit')
def edit_post(request):
    entry_id = request.matchdict['id']
    entry_query = DBSession.query(Entry).get(entry_id)
    form = EntryForm(request.POST, entry_query)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry_query)
        DBSession.add(entry_query)
        DBSession.flush()
        url = request.route_url('entry_route', id=entry_id)
        return HTTPFound(url)
    return {'form': form}


@view_config(route_name='auth', match_param='action=in', renderer='string')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in(request):
    login_form = None
    if request.method == 'Post':
        login_form = LoginForm(request.POST)
    if login_form and login_form.validate():
        user = User.by_name(login_form.username.data)
        if user and user.verify_password(login_form.password.data):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('index_route'),
                     headers=headers)


class EntryForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=128)])
    text = TextAreaField('Content')


class LoginForm(Form):
    username = TextAreaField('Username', [validators.Length(min=1, max=30)])
    password = TextAreaField('Password', [validators.Length(min=1, max=50)])
