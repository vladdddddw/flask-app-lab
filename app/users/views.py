from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from .models import User
from .forms import LoginForm, RegistrationForm

users_bp = Blueprint('users', __name__, template_folder='templates')

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', title='Register', form=form)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.profile'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('users/login.html', title='Login', form=form)

@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    cookies = request.cookies
    theme = request.cookies.get('theme', 'light')
    response = make_response(render_template('users/profile.html', cookies=cookies, theme=theme))
    return response


@users_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('users.login'))


@users_bp.route('/account')
@login_required
def account():

    return render_template('users/profile.html')


@users_bp.route('/set-theme/<theme>')
def set_theme(theme):
    if theme in ['light', 'dark']:
        response = make_response(redirect(request.referrer or url_for('users.profile')))
        response.set_cookie('theme', theme, max_age=60 * 60 * 24 * 30)
    else:
        response = make_response(redirect(request.referrer or url_for('users.profile')))
    return response

@users_bp.route("/hi/<string:name>")
def greetings(name):
    return render_template("users/hi.html", name=name.upper(), age=None)

@users_bp.route("/admin")
def admin():
    return redirect(url_for("users.greetings", name="Administrator"))