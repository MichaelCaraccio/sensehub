# -*- coding: utf-8 -*-

import logging
import logging.config
import datetime
from sensehub import app, db

def drop_all():
    db.drop_all()

def create_all():
    db.create_all()

def conditionnal_seed():
    #TODO CREATE CONDITION
    from db_seed import main as seed
    drop_all()
    try:
        create_all()
        seed()
    except:
        pass #already seeded


def load_git_version(app):
    import subprocess
    try:
        version = subprocess.check_output(["git", "log", '-1', '--pretty=%h %ct'], cwd="/source").decode("utf-8").split(" ")

        version[1] = datetime.datetime.fromtimestamp(
            int(version[1])
        ).strftime('%Y-%m-%d %H:%M:%S')
    except:
        version = "Fail to get version"
    app.config["GITVERSION"] = version


def load_logs(app):
    import os.path

    if not os.path.exists("logs"):
        os.mkdir("logs")

    formatter = logging.Formatter("%(asctime)s %(levelname)s:%(threadName)s:%(name)s : %(message)s")

    info = logging.handlers.RotatingFileHandler("logs/info.log",
                                                maxBytes=1048576,
                                                backupCount=10,
                                                encoding="utf8"
                                                )
    info.setFormatter(formatter)
    info.setLevel(logging.INFO)

    app.logger.addHandler(info)

    error = logging.handlers.RotatingFileHandler("logs/error.log",
                                                 maxBytes=1048576,
                                                 backupCount=10,
                                                 encoding="utf8"
                                                 )
    error.setFormatter(formatter)
    error.setLevel(logging.ERROR)

    app.logger.addHandler(error)


def main():
    #conditionnal_seed()
    import os
    debug = os.environ["DEBUG"] == "True"
    app.run(debug=debug, host="0.0.0.0")


if __name__ == "__main__":
    load_logs(app)
    load_git_version(app)
    main()
