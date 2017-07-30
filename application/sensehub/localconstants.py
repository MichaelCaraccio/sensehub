# -*- coding: utf-8 -*-
import os
server="sensehub_db"
db = os.environ['MYSQL_DATABASE']
user = os.environ['MYSQL_USER']
passwd = os.environ['MYSQL_PASSWORD']

db_address = 'mysql://%s:%s@%s/%s' % (user, passwd, server, db)
salt = os.environ["PASSWORD_SALT"]
