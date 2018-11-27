import config
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

config_name = os.getenv('FLASK_ENV', 'default')

app = Flask(__name__)
app.config.from_object(config.config[config_name])
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

#from drugdev import models
from drugdev.api import api


