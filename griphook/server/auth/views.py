from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, login_required

from griphook.server import db
from griphook.server.auth.models import User
from griphook.server.auth.forms import LoginForm, RegisterForm
from griphook.server.auth.utils import check_user_password_hash

user_blueprint = Blueprint('auth', __name__, )


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash('Thank you for registering.', 'success')
        return redirect(url_for("auth.members"))

    return render_template('auth/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_user_password_hash(user, request.form['password']):
                login_user(user)
                flash('You are logged in. Welcome!', 'success')
                return redirect(url_for('auth.members'))
        flash('Invalid email and/or password.', 'danger')
        return render_template('auth/login.html', form=form)
    return render_template('auth/login.html', title='Please Login', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out. Bye!', 'success')
    return redirect(url_for('main.home'))


@user_blueprint.route('/members')
@login_required
def members():
    return render_template('auth/members.html')
