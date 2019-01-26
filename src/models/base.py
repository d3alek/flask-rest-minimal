from sqlalchemy import Column, DateTime, text
from sqlalchemy.ext.declarative import declarative_base, declared_attr

DEFAULT_TO_UTC = text("TIMEZONE('utc', CURRENT_TIMESTAMP)")

class Updateable(object):
    @declared_attr
    def updated_at(cls):
        return Column(DateTime, server_default=DEFAULT_TO_UTC, onupdate=DEFAULT_TO_UTC)

class CustomBase(object):
    @declared_attr
    def created_at(cls):
        return Column(DateTime, server_default=DEFAULT_TO_UTC)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __hash__(self):
        return hash(self.id)

Base = declarative_base(cls=CustomBase)
