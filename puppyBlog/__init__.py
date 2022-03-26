# puppyBlog/__init__.py 
# import _tkinter
from cmath import log
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

############################
###### DATABASE SETUP ######
############################

basedir = os.path.abspath(os.path.dirname(__file__))
# set up connection to db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

#############################

############ LOGIN CONFIGS ####

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'



#registering my bluprint to link to my app.py 
from puppyBlog.core.views import core 
app.register_blueprint(core)

#linking the 404 and 403 error pages into the app 
from puppyBlog.error_pages.handlers import error_pages
app.register_blueprint(error_pages)

#linking users views Blueprint
from puppyBlog.users.views import users
app.register_blueprint(users)


#linking and registering BLogposts views Blueprint
from puppyBlog.blogposts.views import blog_posts
app.register_blueprint(blog_posts)