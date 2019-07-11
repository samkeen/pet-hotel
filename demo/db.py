import uuid

from flask import current_app, g, Flask
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor


def init_app(app):
    # tells Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(close_db)


def get_db():
    if 'db' not in g:
        app = Flask(__name__)
        mysql = MySQL(cursorclass=DictCursor)

        # MySQL configurations
        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
        app.config['MYSQL_DATABASE_DB'] = 'demo'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        mysql.init_app(app)
        g.db = mysql.connect()
        # g.db = sqlite3.connect(
        #     current_app.config['DATABASE'],
        #     detect_types=sqlite3.PARSE_DECLTYPES
        # )
        # g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def get_uuid():
    return str(uuid.uuid1())

def init_db():
    db = get_db()
    # cur = db.cursor().execute("SHOW DATABASES")
    #
    # for x in cur:
    #     print(x)

    with current_app.open_resource('schema.sql') as f:
        db.cursor().execute(f.read().decode('utf8'))
