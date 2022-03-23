# puppyBlog/__init__.py 

from flask import Flask 

app = Flask(__name__)

#registering my bluprint to link to my app.py 
from puppyBlog.core.views import core 
app.register_blueprint(core)

#linking the 404 and 403 error pages into the app 
from puppyBlog.error_pages.handlers import error_pages
app.register_blueprint(error_pages)