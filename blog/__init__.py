from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from config import *
from flask_login import LoginManager
app= Flask(__name__)
db= SQLAlchemy (app)
app.config.from_object(Config)
migrate= Migrate (app, db)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message= 'Для доступа к данной странице нужно войти в аккаунт'
login_manager.login_message_category = 'info'

from blog import routes, models