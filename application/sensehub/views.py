#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for

from sensehub import app
from sensehub.models import User as User
from flask_login import login_user, logout_user

@app.route("/logout/")
def logout():
    logout_user()
    return redirect("/")

@app.route("/user/<int:user_id>")
def route_user_id(user_id):
    user = User.query.get_or_404(user_id)
    return redirect(url_for("route_user_username", user_username=user.username))


@app.route("/user/<string:user_username>")
def route_user_username(user_username):
    user = User.query.filter_by(username=user_username).first_or_404()
    return render_template("user.html", title=user.username, user=user)

@app.route("/about/")
def route_about():
    return render_template("about.html", title="About", active="About")

@app.route("/")
def route_home():
    return render_template("index.html", title="index", active="Index")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
