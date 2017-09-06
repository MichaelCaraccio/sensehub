# -*- coding: utf-8 -*-
from sensehub import db, login_manager
from sensehub.localconstants import salt
import hashlib
from flask_login import LoginManager, login_user, logout_user
from sensehub.json_type import JsonType

class Salting(object):
    _salt = str(salt.encode('utf-8'))
    _hash = hashlib.sha512

    @staticmethod
    def _salt_pass(password):
        salted = str(Salting._hash(str(password+Salting._salt).encode('utf-8')).hexdigest())
        return salted

    @staticmethod
    def get_salted_password(password):
        return Salting._salt_pass(password)

    @staticmethod
    def is_password_correct(password, salted_password):
        return Salting.get_salted_password(password) == salted_password

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#https://blog.openshift.com/use-flask-login-to-add-user-authentication-to-your-python-application/
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))
    privilege = db.Column(db.Integer)

    def __init__(self, username, password, privilege=0):
        self.username = username
        self.password = Salting.get_salted_password(password)
        self.privilege = privilege

    def __repr__(self):
        return "<User %r>" % self.username

    def __str__(self):
        return self.username

    def get_name(self):
        return self.username

    @property
    def is_active(self):
        ''' needed for flask_login '''
        return True

    @property
    def is_authenticated(self):
        ''' needed for flask_login '''
        return True

    @property
    def is_anonymous(self):
        ''' needed for flask_login '''
        return False

    def get_id(self):
        ''' needed for flask_login '''
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Group %r>" % self.id


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('sensors', lazy='dynamic'))
    name = db.Column(db.String(128))
    key = db.Column(db.String(128))
    hardware_type = db.Column(db.String(128))
    is_public = db.Column(db.Boolean)
    type = db.Column(db.String(20))
    last_ping = db.Column(db.DateTime)
    meta = db.Column(db.Text)
    ip = db.Column(db.String(15))

    def __init__(self, user, name, hardware_type, is_public, type, meta):
        self.user_id = user.id
        self.name = name
        self.hardware_type = hardware_type
        self.is_public = is_public
        self.type = type
        self.meta = meta

    def __repr__(self):
        return "<Sensor %r>" % self.id

class Value(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    sensor = db.relationship('Sensor', backref=db.backref('values', lazy='dynamic'))
    type = db.Column(db.String(128))
    value = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    meta = db.Column(JsonType)

    def __init__(self, sensor, type, value, datetime_obj, meta):
        self.sensor_id = sensor.id
        self.type = type
        self.value = value
        self.timestamp = datetime_obj
        self.meta = meta

    def __repr__(self):
        return "<Value %r>" % self.id

class GroupSensorRelation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
    sensor_id = db.Column('sensor_id', db.Integer, db.ForeignKey('sensor.id'))

    def __init__(self, group, sensor):
        self.group_id = group.id
        self.sensor_id = sensor.id

    def __repr__(self):
        return "<GroupSensorRelation %r>" % self.id

class GroupRoleRelation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    privilege = db.Column('privilege', db.Integer)

    def __init__(self, group, user, privilege=0):
        self.group_id = group.id
        self.user_id = user.id
        self.privilege = privilege

    def __repr__(self):
        return "<GroupRoleRelation %r>" % self.id
