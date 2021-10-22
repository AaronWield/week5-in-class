from flask import Blueprint, render_template, request, url_for, flash, redirect
from drone_inventory.forms import UserLogInForm
from drone_inventory.models import User, db, check_password_hash
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLogInForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

# create (instantiate) a new user class and add that user into the table
        new_user = User(email, password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
# flash message for registration success
        flash(f'You have successfully registered an account and logged in under {email}', 'user-created')
# redirect to home page after signing up
        return redirect(url_for('site.home'))
        
    return render_template('signup.html', form = form)


@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLogInForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email,password)

        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash('You were successfully logged in.', 'auth-success')
# Redirecting upon successful login
            return redirect(url_for('site.home'))
# unsuccessful login
        else:
            flash('Your Email/Password is incorrect', 'auth-failed')
            return redirect(url_for('auth.signin'))
    return render_template('signin.html', form = form)

# Logout, redirects to homepage
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out.', 'auth-success')
    return redirect(url_for('site.home'))

