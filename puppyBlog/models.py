#models.py 

#import db from __init__.py file 
from puppyBlog import db, login_manager 
#allows to hash passwords 
from werkzeug.security import generate_password_hash, check_password_hash
#allows to set up isAuthenticate etc 
from flask_login import UserMixin
from datetime import datetime

#login management 
# allows us to use this in templates for isUser stuff 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    #in the static folder there will be a default image if user does not pick one
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.png')
    #index=True docs.sqlalchemy.org - indexes - has more to do with sql than flask 
    # allows you to make the column into an index 
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # backref is the relationship we have - so the user is the author of the blogpost 
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

#going to use this in our login view 
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"Username {self.username}"

class BlogPost(db.Model):
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True)
    # this comes from the users table - and the id - this is the fkey for our users id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    #date for each blogpost 
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id
    
    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} --- Title: {self.Title}"

