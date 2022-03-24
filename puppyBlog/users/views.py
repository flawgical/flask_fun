# users/views.py 
from crypt import methods
from operator import methodcaller
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from puppyBlog import db
from puppyBlog.models import User, BlogPost
from puppyBlog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from puppyBlog.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__) # dont forget to register this in __init__.py 


# register
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for Registration!')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', form=form)

# login
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in!')
        # grab the info of what the user was trying to do 
            next = request.args.get('next')
            if next==None or not next[0]=='/':
                next = url_for('core.index')
            
            return redirect(next)
    return render_template('login.html', form=form)


# logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index')) #once the user has logged out we will redirect them back home


#account (update UserForm)
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            #grab the current users username and add that profile pic - and pass that in the add_profile_pic function
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic 
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User account updated!!')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)

# users list of blog posts ALL 

@users.route('/<username>')
def user_posts(username):
    # we need to grab the blog posts associated with that user and the page 
    page = request.args.get('page', 1, type=int) #this will help us cycle through users posts using pages - we won't need to have 150 posts in one go - we can cycle through the pages - will be referencing it later on
    user = User.query.filter_by(username=username).first_or_404()  # instead of getting a major error we can pass an error here 
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.data.desc()).paginate(page=page, per_page=5) # foreign key relationship was author for each users' post AND we are requesting pages 5 per page for pagination 
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)

