from datetime import datetime
from jinja2 import Markup
from pyramid.security import Allow, Everyone, Authenticated
import markdown
import sqlalchemy as sa

from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(120))
    text = Column(Unicode)
    created = Column(DateTime, default=datetime.utcnow)

    def __json__(self, request):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'created': self.created.isoformat
        }

    def to_json(self, request=None):
        return self.__json__(request)

    @property
    def rendered_text(self):
        return render_markdown(self.text)

    @classmethod
    def all(cls, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).order_by(sa.desc(cls.created)).all()

    @classmethod
    def by_id(cls, id, session=None):
        if session is None:
            session = DBSession
        return session.quesy(cls).get(id)


class BaseFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'add'),
        (Allow, Authenticated, 'edit'),
    ]

    def __init__(self, request):
        pass


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)

    @classmethod
    def by_name(cls, name, session=None):
        if session is None:
            session = DBSession
        return DBSession.query(cls).filter(cls.name == name).first()


def render_markdown(content):
    marked = Markup(markdown.markdown(content))
    return marked
