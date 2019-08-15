from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from brewit.env2.config import db_config, key
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = key
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=db_config['user'], pw=db_config['password0'], url=db_config['host'], db=db_config['database'])
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from brewit.routes import routes