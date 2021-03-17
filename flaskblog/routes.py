from flask import render_template, redirect, flash, url_for, request
from flaskblog import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
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


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


