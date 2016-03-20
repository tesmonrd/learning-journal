# -*- coding: utf-8 -*-
from pyramid.view import view_config
from .models import Entry, DBSession
from wtforms import Form, StringField, TextAreaField, validators
from pyramid.httpexceptions import HTTPFound
from jinja2 import Markup
import markdown


@view_config(route_name='index_route', renderer='../rick-mockups/list.jinja2')
def post_index(request):
    entries = DBSession.query(Entry).all()
    return {'entries': entries}


@view_config(route_name='entry_route', renderer='../rick-mockups/entry.jinja2')
def view_post(request):
    entry_id = '{id}'.format(**request.matchdict)
    entry_data = DBSession.query(Entry).filter(Entry.id == entry_id).first()
    entry_data.text = render_markdown(entry_data.text)
    return {'entry': entry_data}


@view_config(route_name='new_route', renderer='../rick-mockups/add.jinja2')
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


@view_config(route_name='edit_route', renderer='../rick-mockups/add.jinja2')
def edit_post(request):
    entry_id = request.matchdict['entry']
    entry_query = DBSession.query(Entry).get(entry_id)
    form = EntryForm(request.POST, entry_query)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry_query)
        DBSession.add(entry_query)
        DBSession.flush()
        url = request.route_url('entry_route', id=entry_id)
        return HTTPFound(url)
    return {'form': form}


def render_markdown(content):
    output = Markup(markdown.markdown(content))
    return output


class EntryForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=128)])
    text = TextAreaField('Content')
