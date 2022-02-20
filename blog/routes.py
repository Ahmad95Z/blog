import re
from tokenize import Comment
from turtle import title
from unicodedata import name
from blog import app
from flask import render_template, redirect, request, url_for,flash
from blog.models import Post, db, User,Comment
from flask_login import login_required, login_user, logout_user, current_user
from blog.forms import RegistrationForm, PostForm
from PIL import Image
@app.route('/')
def index():
    page = request.args.get('page',type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('index.html', posts=posts)

@app.route('/new-post', methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()

    if form.validate_on_submit():
        image= request.files.get('image')
        if image:
            file_name= image.filename
            image = Image.open(image)
            image.save('blog/static/img/blog/'+file_name)
            post = Post(title=form.title.data, content=form.content.data, author=current_user,image=file_name)
        db.session.add(post)
        db.session.commit()
        flash('Пост был создан','success')
        return redirect(url_for('index'))   
    return render_template ('new-post.html',form=form)




@app.route('/login', methods =['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(email = request.form.get('email')).first()
        if user and user.password == request.form.get('password'):
            login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
        logout_user()
        return redirect(url_for('index'))

@app.route('/register', methods =['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template ('register.html', form=form)


@app.route('/blog/<int:post_id>',methods=['GET','POST'])
def post_detail(post_id):
    post = Post.query.get(post_id)
    comments=Comment.query.order_by(Comment.date_posted)
    if request.method == 'POST':
       comment = Comment(name=request.form.get('name'), subject=request.form.get('subject'),email=request.form.get('email'),message=request.form.get('message'),post=post)
       db.session.add(comment)
       db.session.commit() 
       redirect (url_for('post_detail',post_id=post.id))
    return render_template('post_detail.html', post=post,comments=comments)

@app.route('/blog/<int:post_id>/del')
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect ('/')
    
@app.route('/blog/<int:post_id>/update',methods=['GET','POST'])
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect ('/')
    else:
        return render_template('update.html', post=post)
    