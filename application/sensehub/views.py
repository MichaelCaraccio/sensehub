#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for

from sensehub import app
from sensehub.models import User as User
from sensehub.models import Sensor as Sensor

from flask_login import login_user, logout_user

@app.route("/logout/")
def logout():
    logout_user()
    return redirect("/")

@app.route("/about/")
def route_about():
    return render_template("pages/about.html", active="About")

@app.route("/sensors/")
def route_sensors():
    return render_template("pages/sensors.html", active="Sensors")

@app.route("/sensor/<int:sensor_id>")
def route_sensor_id(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    return render_template("pages/sensor.html", active="Sensors", sensor=sensor)

@app.route("/sensor/add/")
def route_add_sensor():
    return render_template("pages/add_sensor.html", active="Sensors")

@app.route("/")
def route_home():
    return render_template("pages/index.html", active="Home")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
