# -*- coding: utf-8 -*-

import random, string
from sensehub import db
from sensehub.models import User as User
import passwords

def main():
    for user, password in passwords.passwords.items():
        u = User(user, password)
        db.session.add(u)
        db.session.commit()

if __name__ == '__main__':
    main()
