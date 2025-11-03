from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from app.forms import ContactForm, LoginForm

users_bp = Blueprint('users', __name__, template_folder='templates')


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        if username == 'admin_koroliuk' and password == 'pass123':
            session['username'] = username
            if remember:
                flash(f'Login successful for {username}! We will keep you logged in.', 'success')
            else:
                flash(f'Login successful for {username}!', 'success')

            return redirect(url_for('users.profile'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
            return redirect(url_for('users.login'))  # Post/Redirect/Get

    return render_template('users/login.html', title='Login', form=form)

@users_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('users.login'))

    cookies = request.cookies

    theme = request.cookies.get('theme', 'light')
    response = make_response(render_template('users/profile.html', cookies=cookies, theme=theme))

    if request.method == 'POST':
        action = request.form.get('action')


        if action == 'add':
            key = request.form.get('cookie_key')
            value = request.form.get('cookie_value')
            expiry = request.form.get('cookie_expiry')
            if key and value:
                flash(f"Cookie '{key}' added successfully.", 'success')
                if expiry and expiry.isdigit():
                    response.set_cookie(key, value, max_age=int(expiry))
                else:
                    response.set_cookie(key, value)


        elif action == 'delete':
            key_to_delete = request.form.get('cookie_key_delete')
            if key_to_delete in cookies:
                response.delete_cookie(key_to_delete)
                flash(f"Cookie '{key_to_delete}' has been deleted.", 'info')
            else:
                flash(f"Cookie '{key_to_delete}' not found.", 'warning')


        elif action == 'delete_all':
            for key in cookies.keys():
                if key != 'session':
                    response.delete_cookie(key)
            flash('All other cookies have been deleted.', 'info')


    return response

@users_bp.route('/set-theme/<theme>')
def set_theme(theme):
    if theme in ['light', 'dark']:

        response = make_response(redirect(request.referrer or url_for('users.profile')))

        response.set_cookie('theme', theme, max_age=60*60*24*30)
        flash(f'Theme set to {theme}.', 'info')
    else:
        flash('Invalid theme specified.', 'danger')
        response = make_response(redirect(request.referrer or url_for('users.profile')))
    return response

@users_bp.route('/logout', methods=['POST'])
def logout():

    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('users.login'))

@users_bp.route("/hi/<string:name>")
def greetings(name):

    age = request.args.get("age")

    return render_template("users/hi.html", name=name.upper(), age=age)

@users_bp.route("/admin")
def admin():

    return redirect(url_for("users.greetings", name="Administrator"))