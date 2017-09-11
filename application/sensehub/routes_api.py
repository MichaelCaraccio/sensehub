#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import sys
import os
import base64
import hashlib

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
# Constants
#############################################################

root = '/app/sensehub'
static = 'static'
static_path= root + '/' + static
upload_images = 'uploads/sensor_images'
upload_images_path = static_path + '/' + upload_images
upload_videos = 'uploads/sensor_videos'
upload_videos_path = static_path + '/' + upload_videos


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

def print_flask(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()

def get_value_dict(value):
    '''returns a dict that will be transformed to json'''
    return {
        'sensor_id': value.sensor_id,
        'type': value.type,
        'value': value.value,
        'timestamp':value.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'meta': value.meta
        } if value is not None else {}

def get_sensor_dict(sensor):
    '''returns a dict that will be transformed to json'''
    return {
        'id': sensor.id,
        'user': sensor.user_id,
        'name': sensor.name,
        'hardware_type': sensor.hardware_type,
        'is_public':sensor.is_public,
        'type': sensor.type,
        'last_ping': sensor.last_ping,
        'last_value': get_value_dict(sensor.values.order_by(desc(Value.timestamp)).first())
        }

#############################################################
# Ping
#############################################################


@app.route("/api/ping", methods=["PUT"])
def route_api_ping():
    try:
        form = request.get_json()
        sensor_id = form.get('sensor_id')
        key = form.get('key')
        sensor = authenticate_sensor(sensor_id, key)
        sensor.last_ping = datetime.utcnow()
        return ok_json()
    except ValueError as e:
        return error_json(str(e))


#############################################################
# New Value
#############################################################

def download_image(sensor, json_value):
    # Get Latest image with name sensor_id_image.jpeg
    filename = secure_filename(str(sensor.id) + "_image.jpeg")
    path = os.path.join(upload_images_path, filename)
    filename = url_for(static, filename=path[len(static_path)+1:])
    image_live = get_live_image(filename)

    # Save image in db if does not exist
    if image_live is None:
        value = Value(sensor, json_value['type'], filename, json_value['timestamp'], json_value['meta'])
        db.session.add(value)
        db.session.commit()
    else :
        image_live.timestamp = json_value['timestamp']
        db.session.commit()

    # Save image in Storage
    bytes_array = base64.b64decode(json_value['value'])
    with open(path, "wb+") as fh:
        fh.write(bytes_array)

    # if 'persist' does not exist in json, the second part will not be evaluated
    if 'persist' in json_value['meta'] and json_value['meta']['persist'] == True:
        hashname = hashlib.sha256()
        to_hash = str(sensor.id) + str(datetime.now())
        hashname.update(to_hash.encode('utf-8'))

        filename = str(hashname.hexdigest()) + "_image.jpeg"
        path = os.path.join(upload_images_path, filename)
        with open(path, "wb+") as fh:
            fh.write(bytes_array)

        value = Value(sensor, json_value['type'], url_for(static, filename=path[len(static_path)+1:]), json_value['timestamp'], json_value['meta'])
        db.session.add(value)
        db.session.commit()

def download_video(sensor, json_value):
    # Save video in Storage
    bytes_array = base64.b64decode(json_value['value'])

    hashname = hashlib.sha256()
    to_hash = str(sensor.id) + str(datetime.now())
    hashname.update(to_hash.encode('utf-8'))

    filename = str(hashname.hexdigest()) + "_video.mp4"
    path = os.path.join(upload_videos_path, filename)
    with open(path, "wb+") as fh:
        fh.write(bytes_array)

    value = Value(sensor, json_value['type'], url_for(static, filename=path[len(static_path)+1:]), json_value['timestamp'], json_value['meta'])
    db.session.add(value)
    db.session.commit()

# TODO need to sanitize user input
def parse_json_value(sensor, json_value):
    try:
        if json_value['type'] == 'image':
            download_image(sensor, json_value)
        elif json_value['type'] == 'video':
            download_video(sensor, json_value)
        else:
            value = Value(sensor, json_value['type'], json_value[
                          'value'], json_value['timestamp'], json_value['meta'])
            db.session.add(value)
            db.session.commit()
    except BaseException as e:
        print_flask(e)
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

def get_live_image(filename):
    return Value.query.filter_by(value=filename).first()

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
            to_out.append(get_sensor_dict(sensor))
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
            to_out = [get_value_dict(value)]
            return ok_json(to_out)

        else:
            values = Value.query.filter_by(sensor_id=sensor_id).filter(
                Value.timestamp.between(start, stop)).all()
            to_out = []
            for value in values:
                to_out.append(get_value_dict(value))
            return ok_json(to_out)

    except ValueError as e:
        return error_json(str(e))
