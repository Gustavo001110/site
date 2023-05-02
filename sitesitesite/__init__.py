import sys
from pathlib import Path
import jinja2
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

root_path = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent
app = Flask(__name__.split('.')[0], root_path=root_path)

ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(str(root_path / 'templates')))
template = ENV.get_template('a.html')

app = Flask(__name__, template_folder='templates')


app.config['SECRET_KEY'] = '36a2bf07169aa5abf0b0df1bc17a3a9f'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sla.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faça login para acessar o site'
login_manager.login_message_category = 'alert-warning'


from sitesitesite import routes