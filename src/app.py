import os
import datetime
import base64

from src.models.base import Base
from src.models.security import Role, User
from src.models.todo import Todo, todo_parser, todo_fields

from secret import FLASK_SECRET_KEY, SECURITY_PASSWORD_SALT, ADMIN_EMAIL, ADMIN_API_KEY

from flask_sqlalchemy import SQLAlchemy

from flask_security import Security, SQLAlchemyUserDatastore, login_required
from flask_security.core import current_user
from flask_security.decorators import roles_accepted

from flask_migrate import Migrate

from flask import Flask, jsonify
from flask_restful import abort, Api, Resource, marshal

import flask.json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL'] 
app.secret_key = FLASK_SECRET_KEY
app.config['SECURITY_PASSWORD_SALT'] = SECURITY_PASSWORD_SALT
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_UNAUTHORIZED_VIEW'] = None

db = SQLAlchemy(app, model_class=Base)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
migrate = Migrate(app, db)
api = Api(app)
security = Security(app, user_datastore)

def create_user(role_name, email, api_key):
    role = user_datastore.find_or_create_role(role_name)
    first_user = db.session.query(User).filter(User.email==email).one_or_none()

    if first_user:
        app.logger.warning("First %s already exists. Skip creating it.", role_name)
    else:
        app.logger.info("First %s not found, creating it", role_name) 
        first_user = user_datastore.create_user(email=email, api_key=api_key, confirmed_at=datetime.datetime.now())
        user_datastore.add_role_to_user(first_user, role)

    db.session.commit()

@app.before_first_request
def create_admin():
    create_user("admin", ADMIN_EMAIL, ADMIN_API_KEY)

def get_todo(todo_id):
    todo = db.session.query(Todo).filter(Todo.id==todo_id).one_or_none()
    if not todo:
        abort(404, message="Todo with id %d does not exist" % todo_id)
    return todo

# Todo
# shows a single todo item and lets you delete a todo item
class TodoResource(Resource):
    def get(self, todo_id):
        return marshal(get_todo(todo_id), todo_fields)

    @roles_accepted('admin')
    def delete(self, todo_id):
        todo = get_todo(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return '', 204

    @roles_accepted('admin')
    def put(self, todo_id):
        args = todo_parser.parse_args()
        db.session.query(Todo).filter(Todo.id==todo_id).update(args)
        db.session.commit()
        return marshal(get_todo(todo_id), todo_fields), 201

# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoListResource(Resource):
    def get(self):
        todos = db.session.query(Todo).all()
        return marshal(todos, todo_fields)

    @roles_accepted('admin')
    def post(self):
        args = todo_parser.parse_args()
        todo = Todo(**args)
        db.session.add(todo)
        db.session.commit()
        return marshal(todo, todo_fields), 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoListResource, '/todos')
api.add_resource(TodoResource, '/todos/<int:todo_id>')

@app.route('/hello')
@login_required
def hello():
    return jsonify({'email': current_user.email})

# source: https://flask-login.readthedocs.io/en/latest/#custom-login-using-request-loader
@security.login_manager.request_loader
def load_user_from_request(request):
    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = User.query.filter_by(api_key=api_key.decode('utf-8')).first()
        print(user)
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None

if __name__ == '__main__':
    app.run(debug=True)
