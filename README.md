## Подготовка

Правим виртуална среда с Python 3, активираме я и инсталираме изискванията от `requirements.txt`

```
$ virtualenv venv -p python3
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Инициализираме базата данни. Командите по-долу очакват че има `flask_minimal` Postgresql база данни на `localhost`. Как да я направим:

```
CREATE DATABASE flask_minimal;
```

Ако базата данни е различна промени `DB_URL` променливата.

```
$ export DB_URL="postgresql://locahost/flask_minimal" 
$ export FLASK_APP=src/app.py
$ flask db upgrade
```

... или с една команда

```
$ DB_URL="postgresql://locahost/flask_minimal" FLASK_APP=src/app.py flask db upgrade
```

... или за да принтира само чист SQL без да го изпълнява:

```
$ DB_URL="postgresql://locahost/flask_minimal" FLASK_APP=src/app.py flask db upgrade --sql
```

Тази команда чете миграциите в migrations/versions и ги прилага. Самите миграции са генерирани автоматично от моделите в `src/models/` почти същата команда, но вместо `upgrade` пишем `migrate`:

```
$ DB_URL="postgresql://locahost/flask_minimal" FLASK_APP=src/app.py flask db migrate
```

Правим secret.py файл в основната папка със:

- `FLASK_SECRET_KEY`, `SECURITY_PASSWORD_SALT` със случайни стойности, например получена със:

```
$ python -c 'import os; print(os.urandom(16))'
```

- `ADMIN_EMAIL`, `ADMIN_PASSWORD` с имейла и паролата на админа

## Стартиране

```
$ DB_URL="postgresql://locahost/flask_minimal" FLASK_APP=src/app.py flask run
```

## Използване

```
$ curl http://localhost:5000/todos -d "task=something new" -X POST -v
...
$ curl http://localhost:5000/todos
...
$ curl http://localhost:5000/todos/1
...
$ curl http://localhost:5000/todos/1 -X DELETE -v
...
$ curl http://localhost:5000/todos -d "task=something new 2" -X POST -v
...
$ curl http://localhost:5000/todos/2 -d "task=something different 2" -X PUT -v
...
```

## Допълнителна информация

[Flask RESTful](https://flask-restful.readthedocs.io/)

[Flask Security](https://pythonhosted.org/Flask-Security/)

[flask-migrate](https://flask-migrate.readthedocs.io/en/latest/):
