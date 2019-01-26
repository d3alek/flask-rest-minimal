from .base import Base

from sqlalchemy import Column, Integer, String

from flask_restful import reqparse, fields

class Todo(Base):
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)

todo_parser = reqparse.RequestParser()
todo_parser.add_argument('task')

todo_fields = {
        'id': fields.Integer,
        'task': fields.String
        }


