# # -*- coding: utf-8 -*-
# from learning_journal.views import post_index, view_post
# from pyramid.testing import DummyRequest
# from learning_journal.models import DBSession, Entry


# def test_post_index(dbtransaction, new_entry):
#     test_request = DummyRequest()
#     response_dict = post_index(test_request)
#     response = response_dict['entries']
#     assert response[0] == new_entry


# def test_view_post(dbtransaction, new_entry):
#     test_request = DummyRequest()
#     test_request.matchdict = {'id': new_entry.id}
#     response_dict = view_post(test_request)
#     assert response_dict['entry'] == new_entry


# def test_add_post(dbtransaction, app):
#     results = DBSession.query(Entry).filter(
#         Entry.title == 'TEST' and Entry.text == 'TEST')
#     assert results.count() == 0
#     params = {
#         'title': 'TEST',
#         'text': 'TEST'
#     }
#     app.post('/add', params=params, status='3*')
#     results = DBSession.query(Entry).filter(
#         Entry.title == 'TEST' and Entry.text == 'TEST')
#     assert results.count() == 1


# def test_edit_post(dbtransaction, app, new_entry):
#     new_title = new_entry.title + 'TEST'
#     new_text = new_entry.text + 'TEST'
#     params = {
#         'title': new_title,
#         'text': new_text
#     }
#     app.post('/entries/{}/edit'.format(new_entry.id), params=params, status='3*')
#     results = DBSession.query(Entry).filter(
#         Entry.title == new_title and Entry.text == new_text)
#     assert results.count() == 1


# # server response tests
# def test_add_get(dbtransaction, app):
#     response = app.get('/add')
#     assert response.status_code == 200


# def test_edit_get(dbtransaction, app, new_entry):
#     new_entry_id = new_entry.id
#     response = app.get('/entries/{}/edit'.format(new_entry_id))
#     assert response.status_code == 200


# def test_list_route(dbtransaction, app, new_entry):
#     response = app.get('/')
#     assert response.status_code == 200


# def test_detail_route(dbtransaction, app, new_entry):
#     new_entry_id = new_entry.id
#     response = app.get('/entries/{}'.format(new_entry_id))
#     assert response.status_code == 200
