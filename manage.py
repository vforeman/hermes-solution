# coding: utf-8
from __future__ import unicode_literals

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

from hermes.app import app, db


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
