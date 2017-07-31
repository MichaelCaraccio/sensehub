# -*- coding: utf-8 -*-
import sys
#from imp import reload
#reload(sys)
#sys.setdefaultencoding('utf-8')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_login import LoginManager
from sensehub.localconstants import db_address as db_address

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_address
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disables a warning

# Init
app.config["SECRET_KEY"] = "ThisWebSiteIsLit"  # for WTF-forms and login
app.config["GOOGLE_ANALYTICS"] = ""

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

import sensehub.views
import sensehub.routes_api
import sensehub.views_login
import sensehub.errors
import sensehub.models

db.create_all()
