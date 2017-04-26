Hermes Sample Project
============================

An unpredictably slow service for sending emails for LISNR, inc.


## Problem

With this service, you can create a new email with a post to

    http://[host]/v1/email

and retrieve the email that was created with the ID

    http://[host]/v1/email/[email-id]

but the emails take a long time to be sent.  Currently, the retrieve (Lookup by ID) and create just include the initial attributes and the ID but it would be great if it could respond on create and retrive with the status of the progress for the email being sent.

It would be great if the response would include a status indicating something like pending, in progress, or completed (or failed).


## Setup

To run the project locally, you'll need to install Docker and Docker Compose:

- Install Docker: https://docs.docker.com/engine/installation/
- Install Docker Compose: https://docs.docker.com/compose/install/

Or, for starting it locally, start a local redis instance and set the environment variable `CELERY_BROKER_URL` to something like `redis://[redis-host]:6379/0`.

## Make DB changes

At the root of the project, run

    python manage.py db migrate

to create a new schema and run

    python manage.py db upgrade

to perform the migration in the database.
