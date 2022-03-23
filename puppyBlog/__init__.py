# puppyBlog/__init__.py 

from flask import Flask 

app = Flask(__name__)

#registering my bluprint to link to my app.py 
from puppyBlog.core.views import core 
app.register_blueprint(core)