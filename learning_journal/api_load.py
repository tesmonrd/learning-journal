from learning_journal.models import DBSession, Entry
import json
import os
import requests


def get_response():
    endpoint_url = 'https://sea401d2.crisewing.com/api/export?apikey='
    api_key = os.environ.get('JOURNAL_KEY', '')
    full_url = endpoint_url + api_key
    username = 'tesmonrd'
    params = {"username": username}
    response = requests.get(full_url, params=params)
    return response.text


def get_entries(json_listings):
    listing_collection = []
    for listing in json_listings:
        entry = {
            "title": listing["title"],
            "text": listing["text"],
            "created": listing["created"],
        }
        listing_collection.append(entry)
    return listing_collection


def populate_db(listing):
    entry = Entry(**listing)
    DBSession.add(entry)
    DBSession.flush()


def import_entries():
    results = get_response()
    json_listings = json.loads(results)
    return get_entries(json_listings)


def populate_list_api():
    for entry in import_entries():
        populate_db(entry)
