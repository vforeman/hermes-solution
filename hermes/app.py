# coding: utf-8
from __future__ import unicode_literals

import os
import random
import time

from celery import Celery
from flask import Flask, jsonify, make_response, request
from flask.ext.sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema, validate


APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(APP_DIR)
SQLITE_DB_PATH = os.path.join(PROJECT_DIR, 'db.sqlite')


# CONFIG

class Config(object):
    DEBUG = True
    SECRET_KEY = 'change-me-please'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{path}'.format(path=SQLITE_DB_PATH)
    BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_BROKER_URL')


# APP SETUP

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
celery_app = Celery()
celery_app.config_from_object(Config)


# MODELS

class Email(db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    from_email = db.Column(db.String(80), nullable=False)
    recipient = db.Column(db.String(80), nullable=False)

    def __init__(self, subject, body, from_email, recipient):
        self.subject = subject
        self.body = body
        self.from_email = from_email
        self.recipient = recipient

    def __repr__(self):
        return '<id {}>'.format(self.id)


# SCHEMAS

class EmailSchema(Schema):
    id = fields.Int(dump_only=True)
    subject = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=80))
    body = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=1000))
    from_email = fields.Str(
        required=True,
        validate=validate.Email())
    recipient = fields.Str(
        required=True,
        validate=validate.Email())

email_schema = EmailSchema()


# VIEWS

@app.route('/v1/email', methods=('POST',))
def create_email_view():
    request_data = request.get_json() or {}
    clean_data, errors = email_schema.load(request_data)

    if errors or not clean_data:
        return make_response(
            jsonify(error=errors or 'Bad Request'),
            400)

    email = Email(**clean_data)
    db.session.add(email)
    db.session.commit()

    async_task = super_slow_email_sender.delay(email.id)
    
    # ID of the async task
    # async_task.id

    data = email_schema.dump(email).data
    return jsonify(data=data)


@app.route('/v1/email/<email_id>', methods=('GET',))
def retrieve_email_view(email_id):
    email = Email.query.get(email_id)

    if email is None:
        return make_response(
            jsonify(error='Invalid Email ID: {id}'.format(id=email_id)),
            404)
    
    # If you store the ID of the async_task, you can retrieve it's AsyncResult instance with
    # task_async_result = super_slow_email_sender.AsyncResult([ID])
    #
    # And get the status:
    # task_async_result.status
    #
    # To get the response from the completed task, you can:
    # was_email_sent, error_message = task_async_result.result
    #
    # AsyncResult API Reference: http://docs.celeryproject.org/en/latest/reference/celery.result.html
    

    data = email_schema.dump(email).data
    return jsonify(data=data)


# TASKS

# do not change
@celery_app.task(name='hermes.super_slow_email_sender', bind=True)
def super_slow_email_sender(self, email_id):
    # just cuz'
    email = Email.query.get(email_id)
    seconds_to_wait = random.randrange(10, 60)
    time.sleep(seconds_to_wait)

    was_email_sent = seconds_to_wait % 2 == 0
    error = None

    if was_email_sent % 2 != 0:
        error = 'hit the fan!'

    return was_email_sent, error


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
