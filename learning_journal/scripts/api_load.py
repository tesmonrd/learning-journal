from learning_journal.models import DBSession, Base, Entry
import transaction
import json
import os


def get_response():
    endpoint_url = 'https://sea401d2.crisewing.com/api/export?apikey='
    api_key = os.environ.get('JOURNAL_KEY', '')
    full_url = endpoint_url + api_key
    username = 'tesmonrd'
    params = {"username": username}
    response = requests.get(full_url, params=params)
    return response.text


def import_entries():
    json_entries = json.loads(get_response())
    for json_entry in json_entries:
        entry = Entry()
        entry.title = json_entry['title']
        entry.text = json_entry['text']
        entry.created = json_entry['created']
        with transaction.manager:
            DBSession.add(entry)


def create_session():
    from sqlalchemy import create_engine
    database_url = os.environ.get('DATABASE_URL', None)
    engine = create_engine(database_url)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)


def main():
    create_session()
    import_entries()


if __name__ == "__main__":
    main()
