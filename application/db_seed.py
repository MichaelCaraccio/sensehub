# -*- coding: utf-8 -*-

from datetime import datetime

from sensehub import db
from sensehub.models import User as User
from sensehub.models import Group as Group
from sensehub.models import GroupRoleRelation as GroupRoleRelation
from sensehub.models import GroupSensorRelation as GroupSensorRelation
from sensehub.models import Sensor as Sensor
from sensehub.models import Value as Value
import passwords
import time

def create_users():
    list_users = []
    for user, password in passwords.passwords.items():
        u = User(user, password)
        list_users.append(u)
        db.session.add(u)
        db.session.commit()
    return list_users


def create_groups(users):
    groups = []
    for user in users:
        group = Group("group_%s" % user.username)
        groups.append(group)
        db.session.add(group)
        db.session.commit()

        group_relation = GroupRoleRelation(group, user)
        db.session.add(group_relation)
        db.session.commit()
    return groups

def add_sensor_to_group(sensor, group):
    rel = GroupSensorRelation(group, sensor)
    db.session.add(rel)
    db.session.commit()

def create_sensors(users, groups):
    sensor1 = Sensor(users[0], "Sensor 1",
                     "Hardware type 1", False, "Type 1", "Meta 1")
    db.session.add(sensor1)
    db.session.commit()
    add_sensor_to_group(sensor1, groups[0])


    sensor2 = Sensor(users[1], "Sensor 2",
                     "Hardware type 2", True, "Type 2", "Meta 2")
    sensor2.key = "1234"
    db.session.add(sensor2)
    db.session.commit()
    add_sensor_to_group(sensor2, groups[1])


    sensor3 = Sensor(users[1], "Sensor 3",
                     "Hardware type 2", False, "Type 2", "Meta 2")
    db.session.add(sensor3)
    db.session.commit()
    add_sensor_to_group(sensor3, groups[0])


    sensor4 = Sensor(users[1], "Sensor 4",
                     "Hardware type 2", False, "Type 2", "Meta 2")
    db.session.add(sensor4)
    db.session.commit()
    add_sensor_to_group(sensor4, groups[1])


    sensor5 = Sensor(users[1], "Sensor 5",
                     "Hardware type 2", False, "Type 2", "Meta 2")
    db.session.add(sensor5)
    db.session.commit()
    add_sensor_to_group(sensor5, groups[0])

    return [sensor1, sensor2, sensor3, sensor4, sensor5]


def create_values(sensors):
    for sensor in sensors:
        for i in range(10):
            value = Value(sensor, sensor.type, "Value %d" %
                          i, datetime.utcnow(), "Meta %d" % i)
            db.session.add(value)
            #time.sleep(1)
    db.session.commit()


def main():
    users = create_users()
    groups = create_groups(users)
    sensors = create_sensors(users, groups)
    create_values(sensors)

if __name__ == '__main__':
    main()
