import pytest
from drugdev.models import Contact


@pytest.fixture
def add_user():
    from drugdev import db
    bob = Contact(username='bob', email='bob@bob.com', first_name='bob', last_name='monk')
    db.session.add(bob)
    db.session.commit()


def test_get_contacts(client):
    assert client.get('/api/contacts').status_code == 200


def test_get_contact_pass(client, add_user):
    assert client.get('/api/contact/bob').status_code == 200


def test_get_contact_fail(client, add_user):
    assert client.get('/api/contact/fred').status_code == 403
