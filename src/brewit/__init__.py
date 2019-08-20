from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from brewit.env2.config import db_config, key, mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = key
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=db_config['user'], pw=db_config['password0'], url=db_config['host'], db=db_config['database'])
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_mgr = LoginManager(app)
login_mgr.login_view = 'signin_template'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = mail['user_name']
app.config['MAIL_PASSWORD'] = mail['pw0']
mail = Mail(app)



from brewit.routes import routes