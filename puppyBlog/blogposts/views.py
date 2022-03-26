#blogposts/views 

from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from puppyBlog import db 
from puppyBlog.models import BlogPost
from puppyBlog.blogposts.forms import BlogPostForm

blog_posts = Blueprint('blog_posts', __name__) # register this in __Init__ py 

# Create a blog post 

@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post = BlogPost(title=form.title.data, text=form.text.data, user_id=current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        flash('BLog Post Created')
        print('Blog post was created')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)


# view a single post
@blog_posts.route('/<int:blog_post_id>') #make sure this is an integer 
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id) # this blog post id is not a string - we are querying for an int 
    return render_template('blog_post.html', title=blog_post.title, date=blog_post.date, post=blog_post)



# update a post 

@blog_posts.route('/<int:blog_post_id>/update',methods=['GET','POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()


    if form.validate_on_submit():

        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Blog Post Updated')
        return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post.id))

    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    return render_template('create_post.html',title='Updating',form=form)




# delete post 
@blog_posts.route('/<int:blog_post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post Deleted')
    return redirect(url_for('core.index'))

