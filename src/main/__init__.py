from flask import Flask, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
event.listen(db.engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=on'))

migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = '/'



from main import routes, models


