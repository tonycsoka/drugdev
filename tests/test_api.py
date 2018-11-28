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
    # fred doesn't exist
    assert client.get('/api/contact/fred').status_code == 204


def test_delete_contact(client, add_user):
    assert client.get('/api/contact/bob').status_code == 200
    # delete bob
    assert client.delete('/api/contact/bob').status_code == 200
    # check he's gone
    assert client.get('/api/contact/bob').status_code == 204


def test_save_contact(client):
    # add jim to the db
    data = {'email': 'jim@jim.com', 'last_name': 'greeve', 'first_name': 'jim'}
    client.post('/api/contact/jim', json=data)
    # check he's in there
    assert client.get('/api/contact/jim').status_code == 200


def test_save_contact_fail(client, add_user):
    data = {'email': 'jim@jim.com', 'last_name': 'greeve', 'first_name': 'jim'}
    # Insert of new user will fail, as we already have bob as a username
    assert client.post('/api/contact/bob', json=data).status_code == 405
    # Make sure old bob is still there
    assert client.get('/api/contact/bob').status_code == 200


def test_update_user(client, add_user):
    rv = client.get('/api/contact/bob').get_json()
    assert rv['/api/contact/bob']['last_name'] == 'monk'
    # update bobs last name from monk to mink
    data = {'last_name': 'mink'}
    assert client.put('/api/contact/bob', json=data).status_code == 201
    # check its changed
    rv = client.get('/api/contact/bob').get_json()
    assert rv['/api/contact/bob']['last_name'] == 'mink'
