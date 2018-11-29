from celery import Celery
from drugdev import app, db
from drugdev.models import Contact, Email
import random
import string

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Add a user every 15 seconds.
    sender.add_periodic_task(15.0, add_user.s(), name='add every 15')


@celery.task
def delete_user(username):
    contact = Contact.query.filter_by(username=username).first()
    if contact:
        db.session.delete(contact)
        db.session.commit()


@celery.task
def add_user():
    name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    sname = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    em1 = Email(email=f'{name}-1@gmail.com')
    em2 = Email(email=f'{name}-2@gmail.com')
    contact = Contact(username=name, first_name=name, surname=sname, emails=[em1, em2])
    db.session.add(contact)
    db.session.add(em1)
    db.session.add(em2)
    db.session.commit()
    # delete this entry after 1 minute
    delete_user.apply_async((name,), countdown=60)
