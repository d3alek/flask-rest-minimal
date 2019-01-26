from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from flask_security import UserMixin, RoleMixin

from src.models.base import Base

roles_users = Table('roles_users',
        Base.metadata,
        Column('user_id', Integer, ForeignKey('user.id')),
        Column('role_id', Integer, ForeignKey('role.id')))

class Role(Base, RoleMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)
    description = Column(String(255), nullable=True)

    def __repr__(self):
        return self.name

class User(Base, UserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(String(255), nullable=False)
    active = Column(Boolean, nullable=False)
    confirmed_at = Column(DateTime, nullable=True)
    roles = relationship('Role', secondary=roles_users,
                            backref=backref('users', lazy='dynamic'))

    def __repr__(self):
        return self.email

