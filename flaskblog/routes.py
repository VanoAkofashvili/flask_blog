import os
import secrets
from PIL import Image
from flask import render_template, redirect, flash, url_for, request
from flaskblog import app, db, bcrypt
from .forms import RegistrationForm, LoginForm, UpdateProfileForm
from flaskblog.models import User
from flask_login import login_user, login_required, logout_user, current_user


@app.route("/")
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in!',
              'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))

        else:
            flash('Invalid credentials, Please check email and password', category='danger')

    return render_template('login.html', form=form)


def save_picture(form_picture):
    # remove old profile picture
    old_fn = os.path.join(app.root_path, 'static', 'profile_pics', current_user.image_file)
    if os.path.exists(old_fn):
        os.remove(old_fn)
    r_hex = secrets.token_hex(8)
    p_extension = os.path.splitext(form_picture.filename)[1]
    new_filename = r_hex + p_extension
    i = Image.open(form_picture)

    i.thumbnail((125, 125))

    path = os.path.join(app.root_path, 'static', 'profile_pics', new_filename)

    i.save(path)
    return new_filename


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            new_picture_name = save_picture(form.picture.data)
            current_user.image_file = new_picture_name
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()

        flash('Profile updated successfully', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('account.html', title='Account', form=form, image_file=image_file)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


