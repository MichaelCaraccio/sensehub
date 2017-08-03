#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import sys, os, base64

from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from sensehub import app, db
from sensehub.models import Sensor as Sensor
from sensehub.models import Value as Value
from sensehub.models import GroupSensorRelation as GroupSensorRelation
from sensehub.models import GroupRoleRelation as GroupRoleRelation
from sqlalchemy import desc

from werkzeug.utils import secure_filename


#############################################################
# Utils
#############################################################

def error_json(message):
    return jsonify({"status": "error", "error_value": message})


def ok_json(message=''):
    return jsonify({"status": "ok", "message": message})


def authenticate_sensor(sensor_id, key):
    sensor = Sensor.query.get(sensor_id)
    if sensor is None:
        raise ValueError('Sensor not found.')
    if sensor.key == key:
        return sensor
    else:
        raise ValueError('Could not authenticate sensor')

#############################################################
# Ping
#############################################################


@app.route("/api/ping", methods=["PUT"])
def route_api_ping():
    try:
        form = request.get_json()
        sensor_id = form.get('id')
        key = form.get('key')
        sensor = authenticate_sensor(sensor_id, key)
        sensor.last_ping = datetime.utcnow()
        return ok_json()
    except ValueError as e:
        return error_json(str(e))


#############################################################
# New Value
#############################################################

def parse_json_value(sensor, json_value):
    try:
        if json_value['type'] == 'image':
            root = '/app/sensehub'
            filename = secure_filename(str(sensor.id) + "_image.jpeg")
            path = os.path.join(root + '/static/uploads/sensor_images', secure_filename(filename))
            with open(path, "wb+") as fh:
                fh.write(base64.b64decode(json_value['value']))
            json_value['value'] = path[len(root):]

        value = Value(sensor, json_value['type'], json_value[
                      'value'], json_value['timestamp'], json_value['meta'])
        db.session.add(value)
        db.session.commit()
    except BaseException as e:
        raise ValueError("Could not parse json" + str(e))


@app.route("/api/new_value", methods=["PUT"])
def route_api_new_value():
    try:
        form = request.get_json()
        sensor_id = form['id']
        key = form['key']
        sensor = authenticate_sensor(sensor_id, key)
        parse_json_value(sensor, form['value'])
        return ok_json()
    except ValueError as e:
        return error_json(str(e))

#############################################################
# Get Sensors
#############################################################


def get_public_sensors():
    return Sensor.query.filter_by(is_public=True).all()


def get_owned_sensors(user_id):
    return Sensor.query.filter_by(user_id=user_id).all()


def get_users_groups_sensors(user_id):
    return Sensor.query.join(GroupSensorRelation)\
        .join(GroupRoleRelation, GroupSensorRelation.group_id == GroupRoleRelation.group_id)\
        .filter_by(user_id=user_id)\
        .all()


def get_all_visible_sensors(user_id):
    public_sensors = get_public_sensors()
    owned_sensors = get_owned_sensors(user_id)
    groups_sensors = get_users_groups_sensors(user_id)
    list_sensors = []
    list_sensors += public_sensors
    list_sensors += owned_sensors
    list_sensors += groups_sensors
    set_sensors = set(list_sensors)
    return set_sensors


def has_user_access_to_sensor(user_id, sensor_id):
    sensors = get_all_visible_sensors(user_id)
    return len([sensor for sensor in sensors if sensor.id == sensor_id]) == 1


@app.route("/api/sensors/", methods=["GET"])
@login_required
def route_api_sensors():
    try:
        user_id = current_user.id
        set_sensors = get_all_visible_sensors(user_id)
        to_out = []
        for sensor in set_sensors:
            to_out.append(sensor.id)
        return ok_json(to_out)  # TODO: add some infos

    except ValueError as e:
        return error_json(str(e))


@app.route("/api/sensor/<int:sensor_id>", methods=["GET"])
@login_required
def route_api_sensor(sensor_id):
    try:
        user_id = current_user.id
        if not has_user_access_to_sensor(user_id, sensor_id):
            raise ValueError('You cant see this sensor')

        start = request.args.get('from', None)
        stop = request.args.get('to', None)
        if stop is None or start is None:
            value = Value.query.filter_by(sensor_id=sensor_id).order_by(
                desc(Value.timestamp)).first()
            to_out = [value.value]  # TODO: add some infos
            return ok_json(to_out)

        else:
            values = Value.query.filter_by(sensor_id=sensor_id).filter(
                Value.timestamp.between(start, stop)).all()
            to_out = []
            for value in values:
                to_out.append(value.id)  # TODO: add some infos
            return ok_json(to_out)

    except ValueError as e:
        return error_json(str(e))
