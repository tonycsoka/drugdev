import pytest
import config

import drugdev

@pytest.fixture
def client():
    app = drugdev.app
    client = app.test_client()
    app.config.from_object(config.config['testing'])
    with app.app_context():
        # alternative pattern to app.app_context().push()
        # all commands indented under 'with' are run in the app context
        drugdev.db.create_all()
        yield client  # Note that we changed return for yield, see below for why
        drugdev.db.drop_all()

