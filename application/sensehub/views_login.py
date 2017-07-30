#!/usr/bin/python
# -*- coding: utf-8 -*-
from sensehub import app, db
from .models import User, Salting
from urllib.parse import urlparse, urljoin
from flask import request, flash, abort, render_template, redirect, url_for
from wtforms import Form, BooleanField, StringField, PasswordField, validators

from flask_login import login_user, logout_user

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)],render_kw={"placeholder": "username"})
    password = PasswordField('Password', [validators.Length(min=6, max=35)],render_kw={"placeholder": "pass"})

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    #form = LoginForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        registered_user = User.query.filter_by(username=username).first()
        if registered_user is None:
            flash('Username or password is invalid', 'error')
            return redirect(url_for('login'))
        if not Salting.is_password_correct(password, registered_user.password):
            flash('Username or password is invalid', 'error')
            return redirect(url_for('login'))
        login_user(registered_user)

        flash('Logged in successfully.')

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('route_home'))
    return render_template('login.html', form=form)
    
