from turtle import title
from blog import app
from flask import render_template, redirect, request, url_for,flash
from blog.models import Post, db, User
from flask_login import login_required, login_user, logout_user, current_user
from blog.forms import RegistrationForm, PostForm
from PIL import Image
@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/post-detail')
def post():
    return render_template('post_detail.html')


@app.route('/login', methods =['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(email = request.form.get('email')).first()
        if user and user.password == request.form.get('password'):
            login_user(user)
        return redirect(url_for('registration'))
    return render_template('login.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
        logout_user()
        return redirect(url_for('index'))

@app.route('/register',methods=['GET','POST'])
def registration():
    if current_user.is_authenticated:
        return redirect  (url_for('index'))
    
    form= RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались','succsess')
        return redirect (url_for('login'))
    return render_template ('register.html', form=form)




@app.route('/logout', methods = ['GET', 'POST'])
def log_out():
    logout_user()
    return redirect(url_for('index'))

@app.route('/blog/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get(post_id)
    return render_template('post_detail.html', post=post)